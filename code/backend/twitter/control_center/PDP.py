## @package twitter.control_center
# coding: UTF-8
import random
import datetime
import json
import logging
from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI
from wrappers.postgresql_wrapper import PostgresAPI
from control_center.policies_types import PoliciesTypes
import log_actions
from control_center.intelligence import classifier
import numpy as np

# Constants used below for the Heuristics
THRESHOLD_LIKE = 0.4
THRESHOLD_RETWEET = 0.6
THRESHOLD_REPLY = 0.6
THRESHOLD_FOLLOW_USER = 0.85
POLICY_KEYWORDS_MATCHES = 0.2
POLICY_USER_IS_TARGETED = 0.4
PENALTY_LIKED_RECENTLY_SMALL = -0.35
PENALTY_LIKED_RECENTLY_SMALL_INTERVAL = 10
PENALTY_LIKED_RECENTLY_LARGE = -0.65
PENALTY_LIKED_RECENTLY_LARGE_INTERVAL = 5
PENALTY_RETWEETED_USER_RECENTLY = -0.5
PENALTY_RETWEETED_USER_RECENTLY_INTERVAL = 43200  # 12 hours
PENALTY_REPLIED_USER_RECENTLY_INTERVAL = 24 * 60 * 60  # a day
PENALTY_REPLIED_USER_RECENTLY = -0.5
BOT_FOLLOWS_USER = 0.3
BOT_RETWEETED_TWEET = 0.2
BOT_LIKED_TWEET = 0.3

LIMIT_REPLY_LOGS_QUANTITY = 1000

log = logging.getLogger('PDP')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(open("pdp.log", "w"))
handler.setFormatter(logging.Formatter(
    "[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

log = logging.getLogger('PDP')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("pdp.log", "w"))
handler.setFormatter(logging.Formatter(
    "[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class PDP:
    def __init__(self):
        '''
        Here starts the connections with the other DB wrappers
        '''
        self.mongo = MongoAPI()
        self.neo4j = Neo4jAPI()
        self.postgres = PostgresAPI()

    def receive_request(self, data):
        # Leaving this as a simple function call, leaving the room for handling the data available
        return self.evaluate(data)

    def evaluate(self, msg):
        """
        Workflow of this function:
            1. pre-processing of request (filter, prepare db request, etc)
            2. request to DB
            3. get request from DB
            4. post-processing of response (clean response from db, etc)
            5. DECIDE (PERMIT, DENY)

        @param msg : dict
            Dictionary with necessary fields to perform the query.
            Something of this form: { "type" : action, data }

        @return response:
            A response with either "DENY" or "PERMIT"
        """

        evaluate_answer = False
        # PRE-PROCESSING the request to get the QUERY
        '''
        prepare the query according to the request
        for all REQUEST_TWEET*, it's based on a heuristic (if it's in the threshold, request accepted): 0 to 1
        if it's a REQUEST_FOLLOW_USER, check the rules to see if it is accepted
        if it's a first time user, give some usernames
        '''
        msg_type = msg["type"]

        if msg_type == PoliciesTypes.REQUEST_TWEET_LIKE:
            '''
            bot_id
            user_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            res = self.analyze_tweet_like(msg)
            evaluate_answer = res > THRESHOLD_LIKE
        elif msg_type == PoliciesTypes.REQUEST_TWEET_RETWEET:
            '''
            bot_id
            user_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            res = self.analyze_tweet_retweet(msg)
            evaluate_answer = res > THRESHOLD_RETWEET
        elif msg_type == PoliciesTypes.REQUEST_TWEET_REPLY:
            '''
            bot_id 
            user_id       
            tweet_id
            tweet_text
            tweet_entities
            tweet_in_reply_to_status_id_str
            tweet_in_reply_to_user_id_str
            tweet_in_reply_to_screen_name
            '''
            evaluate_answer = self.analyze_tweet_reply(msg) > THRESHOLD_REPLY
        elif msg_type == PoliciesTypes.REQUEST_FOLLOW_USER:
            '''
            bot_id
            user_id

            workflow of this request:

            1- Check bot and its policies
                1.1- if filter=target and target=tweet_user_id:
                        return PERMIT
                1.2- if other_bots.filter=target and other_bots.target=tweet_user_id:
                        return DENY
                1.3- No one has this target
                        GOTO Rule 2

            2- Check neo4j
                2.1- Bot already follows tweet_user_id (this case should never happen, just here for precaution)
                        return DENY
                2.2- Other bot is following tweet_user_id: (questionable, should be discussed)
                        return DENY
                2.3- No one follows tweet_user_id:
                        return PERMIT
            '''
            evaluate_answer = self.analyze_follow_user(msg) > THRESHOLD_FOLLOW_USER
        if evaluate_answer:
            log.info(f"Request to {msg_type.name} accepted")
            return self.send_response({"response": "PERMIT"})
        else:
            log.warning(f"Request to {msg_type.name} denied")
            return self.send_response({"response": "DENY"})

    def send_response(self, msg):
        # json dumps da decisão
        message = json.dumps(msg)
        return message

    def get_first_time_list(self):
        """
        When a bot connects for the first time to Twitter, he'll have to start following people This is the old way:
        having a set list of possible users and the bot will follow a random group from those followers In future
        iterations we may alter this so that there are possible branches a bot could start with: politics,
        football fan, etc., each branch with a list of possible users to follow

        @return: List of users the bot will start following
        """
        log.info(f"Creating users for the bot to start following")
        num_users = 6  # random.randint(2, 10)
        with open("first_time_users.json", "r") as f:
            users = json.load(f)

        bot_list = []
        while len(bot_list) < num_users:
            index = random.randint(0, len(users) - 1)
            bot_list.append(users.pop(index))

        log.info("Sending first time list: " + ", ".join(bot_list))

        return bot_list

    def _bot_is_targeted(self, policy, data):
        """
        Private function to check if a bot is being targeted in a policy
        Checks first if the bot was mentioned in the tweet, or if the user who posted the tweet is himself listed
        in the policy

        @param Policy dictionary containing its information
        @param Data dictionary containing important information

        @returns True or False depending if the bot was indeed targeted
        """
        for mention in data["tweet_entities"]["user_mentions"]:
            if mention["id"] in policy["bots"]:
                log.info(f"Bot <{data['bot_id']}> was mentioned by user")
                return True

        if data["user_id"] in policy["bots"]:
            log.info(f"Bot <{data['bot_id']}> was targeted in the policy")

        log.info(f"Bot <{data['bot_id']}> was not targeted in the policy")
        return False

    def _tweet_has_keywords(self, policy, data):
        """
        Private function to check if a tweet uses any important keywords, be it hashtags or commonly found words

        @param Policy dictionary containing its information
        @param Data dictionary containing important information

        @returns True or False depending if the tweet has keywords
        """
        for hashtag in data["tweet_entities"]["hashtags"]:
            if hashtag["text"] in policy["params"]:
                return True

        for keyword in policy["params"]:
            if keyword in data["tweet_text"]:
                return True

        log.info(f"Tweet <{data['tweet_id']}> has no keywords")
        return False

    def _score_for_relation(self, data):
        """
        Algorithm to attribute a score if there's a follow relationship between the user and the bot

        @param: data - dictionary containing the data of the bot and the tweet to be analyzed
        @returns: float corresponding for the constant attributed to the situation
        """

        type1 = "Bot" if self.neo4j.check_bot_exists(data["bot_id"]) else "User"
        type2 = "Bot" if self.neo4j.check_bot_exists(data["user_id"]) else "User"
        relation_exists = self.neo4j.check_follow_exists({
            "id_1": data["bot_id"],
            "type_1": type1,
            "id_2": data["user_id"],
            "type_2": type2
        })
        if relation_exists:
            log.info(f"Relation exists between {data['bot_id']} and {data['user_id']}")
            return BOT_FOLLOWS_USER
        log.info(f"Relation doesn't exist between {data['bot_id']} and {data['user_id']}")
        return 0

    def _score_for_policies(self, data):
        """
        Algorithm to atribute a score for the relation the bot and the user have with the policies
        If the bot is being targeted by some policy, or if the tweet has a special keyword, it will return the
        appropriate score

        @param: data - dictionary containing the data of the bot and the tweet to be analyzed
        @returns: float corresponding for the constant attributed to the situation
        """
        policy_list = self.postgres.search_policies({
            "bot_id": data["bot_id"]
        })

        # TODO -> TIRAR ESTE PRINT E SUBSTITUIR POR UM LOG
        log.debug(policy_list)

        if policy_list['success']:
            for policy in policy_list["data"]:

                if policy["filter"] == "Target":
                    # Check if our bot is being targeted

                    if self._bot_is_targeted(policy, data):
                        log.debug(f"Bot <{data['bot_id']}> has been targeted by a policy")
                        return POLICY_USER_IS_TARGETED

                elif policy["filter"] == "Keywords":
                    # Check if tweet has any important keywords (be it a hashtag or a commonly found word)

                    if self._tweet_has_keywords(policy, data):
                        log.debug(f"Tweet <{data['tweet_id']}> has been keywords")
                        return POLICY_KEYWORDS_MATCHES

        return 0

    def analyze_tweet_like(self, data):
        """
        Algorithm to analyse if a bot should like a Tweet
        Takes the current statistics and turns them into a real value

        @param: data - dictionary containing the data of the bot and the tweet it wants to like
        @returns: float that will then be compared to the threshold previously defined
        """

        heuristic_value = 0

        # Verify if there's a relation between the bot and the user
        heuristic_value += self._score_for_relation(data)

        # Next we check if the bot and the user have some policies in common
        heuristic_value += self._score_for_policies(data)

        # We then check if the bot has retweeted the tweet
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.RETWEET,
            "target_id": data["tweet_id"]
        })

        if bot_logs['success']:
            log.info("Bot has already retweeted the tweet")
            heuristic_value = heuristic_value + BOT_RETWEETED_TWEET if heuristic_value < 0.8 else 1

        # We now check if the last recorded like from a tweet of this user was too recent

        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.TWEET_LIKE
        })
        if bot_logs['success']:
            for bot_log in bot_logs['data']:
                user_of_tweet_liked = self.mongo.search(
                    collection="tweets",
                    query={"id": bot_log["target_id"]},
                    fields=["user"],
                    single=True
                )
                if user_of_tweet_liked == data["user_id"]:
                    date = bot_log["timestamp"]
                    now = datetime.datetime.now()
                    if (now - date).seconds < PENALTY_LIKED_RECENTLY_LARGE_INTERVAL:
                        log.info("Bot has recently liked a tweet from the same user")
                        heuristic_value += PENALTY_LIKED_RECENTLY_LARGE
                    elif (now - date).seconds < PENALTY_LIKED_RECENTLY_SMALL_INTERVAL:
                        log.info("Bot has liked a tweet from the same user, but may not be that suspicious")
                        heuristic_value += PENALTY_LIKED_RECENTLY_SMALL

        return heuristic_value

    def analyze_tweet_retweet(self, data):
        """
        Algorithm to analyse if a bot should retweet a Tweet
        Takes the current statistics and turns them into a real value

        @param: data - dictionary containing the data of the bot and the tweet it wants to like
        @returns: float that will then be compared to the threshold previously defined
        """

        heuristic_value = 0
        # Verify if there's a relation between the bot and the user
        heuristic_value += self._score_for_relation(data)

        # Next we check if the bot and the user have some policies in common
        heuristic_value += self._score_for_policies(data)

        # We then check if the bot has liked the tweet
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.TWEET_LIKE,
            "target_id": data["tweet_id"]
        })
        if bot_logs["success"]:
            log.info("Bot already liked the tweet")
            heuristic_value = heuristic_value + BOT_LIKED_TWEET if heuristic_value < 0.7 else 1

        # Finally check if the bot already retweeted something from the user too recently
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.RETWEET
        })
        if bot_logs['success']:
            for bot_log in bot_logs['data']:
                user_of_retweet = self.mongo.search(
                    collection="tweets",
                    query={"id": bot_log["target_id"]},
                    fields=["user"],
                    single=True
                )
                if user_of_retweet == data["user_id"]:
                    date = bot_log["timestamp"]
                    now = datetime.datetime.now()
                    if (now - date).seconds < PENALTY_RETWEETED_USER_RECENTLY_INTERVAL:
                        log.debug("Bot has recently retweet the user")
                        heuristic_value += PENALTY_RETWEETED_USER_RECENTLY

        return heuristic_value

    def analyze_tweet_reply(self, data):
        """
        Algorithm to analyse if a bot should reply
        Takes the current statistics and turns them into a real value

        @param: data - dictionary containing the data of the bot and the tweet it wants to like
        @returns: float that will then be compared to the threshold previously defined
        """
        """
                Algorithm to analyse if a bot should retweet a Tweet
                Takes the current statistics and turns them into a real value

                @param: data - dictionary containing the data of the bot and the tweet it wants to like
                @returns: float that will then be compared to the threshold previously defined
                """
        # first, we verify if the bot already replied to the tweet
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.TWEET_REPLY,
            "target_id": data["tweet_id"]
        })
        if not bot_logs["success"] or bot_logs['data']:
            return 0

        heuristic_value = 0
        # Verify if there's a relation between the bot and the user
        heuristic_value += self._score_for_relation(data)

        # Next we check if the bot and the user have some policies in common
        heuristic_value += self._score_for_policies(data)

        # We then check if the bot has liked the tweet
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.TWEET_LIKE,
            "target_id": data["tweet_id"]
        })
        if bot_logs["success"]:
            log.info("Bot already liked the tweet")
            heuristic_value = heuristic_value + BOT_LIKED_TWEET if heuristic_value < 0.7 else 1

        # Finally check if the bot already replied to the user recently
        bot_logs = self.postgres.search_logs({
            "bot_id": data["bot_id"],
            "action": log_actions.TWEET_REPLY
        }, limit=LIMIT_REPLY_LOGS_QUANTITY)

        if bot_logs['success']:
            for bot_log in bot_logs['data']:
                user_of_reply = self.mongo.search(
                    collection="tweets",
                    query={"id": bot_log["target_id"]},
                    fields=["user"],
                    single=True
                )
                if user_of_reply == data["user_id"]:
                    date = bot_log["timestamp"]
                    now = datetime.datetime.now()
                    if (now - date).seconds < PENALTY_REPLIED_USER_RECENTLY_INTERVAL:
                        log.debug("Bot recently replied to another tweet from user")
                        heuristic_value += PENALTY_REPLIED_USER_RECENTLY
                        break

        return heuristic_value

    def analyze_follow_user(self, data):
        """
        Algorithm to analyse if a bot should follow
        Takes the current statistics and turns them into a real value

        @param: data - dictionary containing the data of the bot and the tweet it wants to like
        @returns: float that will then be compared to the threshold previously defined
        """

        heuristic = 0

        MODEL_PATH = "control_center/intelligence/models"

        bot_id = data['bot_id']

        policies = self.postgres.search_policies({
            "bot_id": bot_id, "filter": "Keywords"
        })

        if policies['success']:
            policy_list = policies['data']
            log.debug(f"Obtained policies: {policy_list}")

            if len(policy_list) > 0:
                policy_labels = {}
                for policy in policy_list:
                    policy_labels[policy['name']] = policy['params']

                tweets = data['tweets']
                user = data['user']
                user_description = user['description']
                tweets_text = [t['full_text'] for t in tweets]

                labels = classifier.predict_soft_max(model_path=MODEL_PATH, x=tweets_text + [user_description],
                                                     confidence_limit=THRESHOLD_FOLLOW_USER)
                policies_confidence = {}

                for label in labels:
                    confidence, policy_name = label
                    if policy_name not in policies_confidence:
                        policies_confidence[policy_name] = []
                    policies_confidence[policy_name].append(confidence)

                final_choices = {}

                for key in policies_confidence:
                    mean = np.mean(policies_confidence[key])
                    final_choices[key] = {
                        'mean': mean,
                        'length': len(policies_confidence[key]),
                        'final_score': mean * len(policies_confidence[key]) if mean > 0 else
                        len(policies_confidence[key])
                    }

                best_choice = sorted(list(final_choices.items()), reverse=True, key=lambda c: c[-1]['final_score'])[0]
                picked_label, mean_score = best_choice[0], best_choice[-1]['mean']

                if picked_label in policy_labels:
                    heuristic += mean_score
        log.debug(f"Request to follow user with id: {user['id']} and name {user['name']} "
                  f"{'Accepted' if heuristic > THRESHOLD_FOLLOW_USER else 'Denied'}")
        return heuristic

    def close(self):
        self.neo4j.close()
