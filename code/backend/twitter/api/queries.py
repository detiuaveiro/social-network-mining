import logging
from datetime import datetime, timedelta
from django.db.models import Max, Count, Sum, Q
from api.models import *
import api.serializers as serializers
from api import neo4j
import json
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from api.queries_utils import paginator_factory, paginator_factory_non_queryset, process_neo4j_results
from api.views.utils import NETWORK_QUERY
from report.report_gen import Report
from api.cache_manager import RedisAPI
from api.cache_decorator import cache
import pickle

logger = logging.getLogger('queries')

cacheAPI = RedisAPI()


def update_per_table(cache_manager, model_name):
    keys = filter(lambda k: model_name == k['model_name'],
                  map(lambda k: pickle.loads(k), cache_manager.client.scan_iter()))

    for key in keys:
        encoded_key = pickle.dumps(key)
        data = cache_manager.get(encoded_key)
        func = eval(f"{key['function_name']}")
        cache_manager.delete_key(encoded_key)

        if data['pagination']:
            status, n_data, message = func(*key['args'], **key['kwargs'])

            if status:
                new_data = {
                    'data': n_data,
                    'message': message
                }

                cache_manager.set(encoded_key, new_data)
            else:
                cache_manager.set(encoded_key, data)

        else:
            last_id = data['data']['last_id']
            key['kwargs']['last_id'] = last_id

            status, n_data, message = func(*key['args'], **key['kwargs'])
            if status:
                entries_dict = {}
                for entry in data['data']['entries']:
                    entries_dict[entry.pop('date')] = entry

                for entry in n_data['entries']:
                    date = entry.pop('date')
                    general = entry

                    if date not in entries_dict:
                        empty_counter = {}
                        for entity in general:
                            empty_counter[entity] = 0
                        entries_dict[date] = empty_counter

                    current_counter = entries_dict[date]
                    for entity in current_counter:
                        current_counter[entity] += general[entity]
                    entries_dict[date] = current_counter

                entries = []
                for date in entries_dict:
                    entries.append({
                        **entries_dict[date],
                        'date': date
                    })

                new_data = {
                    'message': data['message'],
                    'data': {
                        'last_id': n_data['last_id'],
                        'entries': entries
                    },
                    'pagination': False
                }

                cache_manager.set(encoded_key, new_data)
            else:
                cache_manager.set(encoded_key, data)


def next_id(model):
    max_id = model.objects.aggregate(Max('id'))['id__max']
    if not max_id:
        max_id = 0

    return max_id + 1


# -----------------------------------------------------------
# users
# -----------------------------------------------------------
def twitter_users_count():
    """
    Returns: Number of  users saved on the mongo database wrapped on a dictionary
    """
    try:
        all_users_count = User.objects.all().count()

        return True, {'count': all_users_count}, "Success obtaining the number of users"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_count.__name__} -> {e}")
        return False, None, "Error obtaining the number of users"


def twitter_users(entries_per_page, page, protected):
    """
    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None
    Returns: Users saved on the mongo database wrapped on a dictionary divided per pages
    if entries_per_page and page are both None then all users will be returned
    """
    try:

        all_users = User.objects.filter(protected=protected)

        data = paginator_factory(all_users, entries_per_page, page)
        data['entries'] = [serializers.User(user).data for user in data['entries']]

        return True, data, "Success obtaining users info"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users.__name__} -> {e}")
        return False, None, f"Error obtaining users info"


def twitter_user(user_id):
    """
    Args:
        user_id: User's ID

    Returns: User info defined by user_id parameter wrapped on a dictionary

    """
    try:
        return True, serializers.User(
            User.objects.get(user_id=user_id)).data, f"Success obtaining user (id:{user_id})"

    except User.DoesNotExist as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user.__name__} -> {e}")
        return False, None, f"User (id:{user_id}) does not exists on database"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user.__name__} -> {e}")
        return False, None, f"Error obtaining user (id:{user_id})"


def twitter_users_stats(entries_per_page, page, protected):
    """

    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None
        protected:  Boolean to identify a protected user

    Returns: Stats saved on the postgres database wrapped on a dictionary divided per pages
    if entries_per_page and page are both None then all stats will be returned
    """
    try:

        stats = UserStats.objects.filter(protected=protected)

        data = paginator_factory(stats, entries_per_page, page)
        data['entries'] = [serializers.UserStats(us).data for us in data['entries']]

        return True, data, "Success obtaining users stats info"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_stats.__name__} -> {e}")
        return False, None, "Error obtaining users stats info"


def twitter_user_stats(user_id, entries_per_page, page):
    """

    Args:
        user_id: User's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: User's stats wrapped  on a dictionary divided per pages
    if entries_per_page and page are both None then all stats will be returned

    """
    try:

        user_stats = UserStats.objects.filter(user_id=user_id)

        data = paginator_factory(user_stats, entries_per_page, page)
        data['entries'] = [serializers.UserStats(stat).data for stat in data['entries']]

        return True, data, f"Success obtaining user's (id:{user_id}) stats"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats.__name__} -> {e}")
        return False, None, f"Error obtaining user's (id:{user_id}) stats"


def twitter_user_stats_grouped(user_id, types):
    """

    Args:
        user_id: User's ID
        types: Group labels (day,month,year)

    Returns: User's stats  grouped by (day or month or year) wrapped on dictionary

    """
    try:
        start_date = UserStats.objects.filter(user_id=user_id).order_by('timestamp').values('timestamp')[0]['timestamp']

        query = "UserStats.objects.filter(Q(user_id=user_id) & Q(followers__gt=0)  & Q(following__gt=0))"
        for group_type in types:
            query += f".annotate({group_type}=Extract{group_type.title()}('timestamp'))"

        order_by_list = [f"'{group_type}'" for group_type in types]
        query += f".values({','.join(order_by_list)}).annotate(sum_followers=Max('followers'), sum_following=Max('following')).order_by({','.join(order_by_list)})"

        users_stats = []
        for obj in list(eval(query)):
            full_date = '/'.join(str(obj.pop(group_type)) for group_type in types)
            obj['full_date'] = full_date
            users_stats.append(obj)

        return True, {'data': users_stats, 'start_date': start_date}, \
               f"Success obtaining user's (id:{user_id}) stats grouped"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_stats_grouped.__name__} -> {e}")
        return False, None, f"Error obtaining user's (id:{user_id}) stats grouped"


def twitter_user_tweets(user_id, entries_per_page, page):
    """

    Args:
        user_id: User's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: User's tweets wrapped  on a dictionary divided per pages
    if entries_per_page and page are both None then all tweets will be returned

    """
    try:

        tweets_id = neo4j.get_tweets_written({'id': user_id})
        user_tweets = Tweet.objects.filter(tweet_id__in=tweets_id).order_by('-created_at')

        data = paginator_factory(user_tweets, entries_per_page, page)
        data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

        return True, data, f"Success obtaining user's (id:{user_id}) tweets"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_tweets.__name__} -> {e}")
        return False, None, f"Error obtaining user's (id:{user_id}) tweets"


def twitter_user_followers(user_id, entries_per_page, page):
    """

    Args:
        user_id: User's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: User's followers wrapped  on a dictionary divided per pages
    if entries_per_page and page are both None then all followers will be returned

    """
    try:
        followers = neo4j.get_followers({'id': user_id})

        data = paginator_factory_non_queryset(followers, entries_per_page, page)

        return True, data, f"Success obtaining users's (id:{user_id}) followers"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_followers.__name__} -> {e}")
        return False, None, f"Error obtaining users's (id:{user_id}) followers"


def twitter_user_following(user_id, entries_per_page, page):
    """

    Args:
        user_id: User's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: User's following wrapped  on a dictionary divided per pages
    if entries_per_page and page are both None then all following will be returned

    """
    try:
        following = neo4j.get_following({'id': user_id})

        data = paginator_factory_non_queryset(following, entries_per_page, page)

        return True, data, f"Success obtaining users's (id:{user_id}) following"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_user_following.__name__} -> {e}")
        return False, None, f"Error obtaining users's (id:{user_id}) following"


def twitter_search_users(keywords, protected, entries_per_page, page):
    """

    Args:
        keywords: Words to be searched
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: User's  that matches keywords on name and screen_name wrapped on response's object divided by pages
    if entries_per_page and page are both None then all users will be returned

    """
    try:
        query_filters = Q()
        for word in keywords.split():
            query_filters |= Q(name__icontains=word) | Q(screen_name__icontains=word)

        users = User.objects.filter(query_filters)
        if protected:
            users = users.filter(protected=True)

        data = paginator_factory(users, entries_per_page, page)
        data['entries'] = [serializers.User(user).data for user in data['entries']]

        return True, data, f"Success searching users by {keywords}"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_search_users.__name__} -> {e}")
        return False, None, f"Error searching users by {keywords}"


def twitter_search_users_strict(keyword, user_type):
    """

    Args:
        keyword: Words to be searched
        user_type: Types of users

    Returns: User's  that matches keywords on name and screen_name wrapped on response's object divided by pages
    if entries_per_page and page are both None then all users will be returned

    """
    try:
        query_params = Q()
        bot_query_params = Q()
        for bot in neo4j.search_bots():
            if bot["username"].lower().startswith(keyword.lower()):
                bot_query_params |= Q(user_id=bot["id"])

        if user_type == "Bot":
            if len(bot_query_params) == 0:
                return True, [], f"Success searching users by {keyword}"
            users = User.objects.filter(bot_query_params)
        else:
            query_params = Q(screen_name__istartswith=keyword)
            users = User.objects.filter(query_params).exclude(bot_query_params)

        user_serializer = [serializers.User(user).data for user in users]

        data = [{
            "id": user["user_id"], "screen_name": user["screen_name"], "name": user["name"]
        } for user in user_serializer]

        return True, data, f"Success searching users by {keyword}"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: "
                     f"Function {twitter_search_users_strict.__name__} -> {e}")
        return False, None, f"Error searching {user_type}s by {keyword}"


def twitter_users_type(user_id):
    """
    Args:
        user_id: User's ID

    Returns: User's type wrapped on dictionary

    """
    try:
        node_type = neo4j.node_type({'id': user_id})
        return True, {'type': node_type}, f"Success obtaining user's (id:{user_id}) type"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_users_type.__name__} -> {e}")
        return False, None, f"Error obtaining user's (id:{user_id}) type"


# -----------------------------------------------------------
# tweets
# -----------------------------------------------------------

def twitter_tweets(entries_per_page, page):
    """

    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All tweets saved on databases wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all tweets will be returned
    """
    try:
        all_tweets = Tweet.objects.all().order_by('-created_at')

        data = paginator_factory(all_tweets, entries_per_page, page)
        data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

        return True, data, "Success obtaining tweets"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets.__name__} -> {e}")
        return False, None, "Error obtaining tweets"


def twitter_tweets_stats(entries_per_page, page):
    """

    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All tweets stats saved on databases wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all tweets stats will be returned

    """
    try:
        tweet_stats = TweetStats.objects.all()

        data = paginator_factory(tweet_stats, entries_per_page, page)
        data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']]

        return True, data, "Success obtaining tweets stats"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets_stats.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweets_stats.__name__} -> {e}")
        return False, None, "Error obtaining tweets stats"


def twitter_tweet(tweet_id):
    """

    Args:
        tweet_id: Tweet's ID

    Returns: Tweet info wrapped  on response's dictionary

    """
    try:
        tweet = Tweet.objects.get(tweet_id=tweet_id)

        return True, serializers.Tweet(tweet).data, f"Success obtaining tweet's (id:{tweet_id}) info"

    except Tweet.DoesNotExist as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet.__name__} -> {e}")
        return False, None, f"Tweet (id:{tweet_id}) does not exist on database"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet.__name__} -> {e}")
        return False, None, f"Error obtaining tweet's (id:{tweet_id}) info"


def twitter_tweet_stats(tweet_id, entries_per_page, page):
    """

    Args:
        tweet_id: Tweet's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: Tweet's stats wrapped on dictionary divided by pages
    if entries_per_page and page are both None then tweet's stats will be returned
    """
    try:
        stats = TweetStats.objects.filter(tweet_id=tweet_id).order_by('-timestamp')

        data = paginator_factory(stats, entries_per_page, page)
        data['entries'] = [serializers.TweetStats(tweet).data for tweet in data['entries']]

        return True, data, f"Success obtaining tweet's (id:{tweet_id}) stats"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_tweet_stats.__name__} -> {e}")
        return False, None, f"Error obtaining tweet's (id:{tweet_id} stats"


def twitter_tweet_replies(tweet_id):
    """

    Args:
        tweet_id: Tweet's ID

    Returns: Tweet's replies wrapped on dictionary

    """
    try:
        all_tweets = Tweet.objects.filter(in_reply_to_status_id_str=tweet_id).order_by('-created_at')

        data = [serializers.Tweet(tweet).data for tweet in all_tweets]

        return True, data, f"Success obtaining all tweet's (id:{tweet_id}) replies"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: "
                     f"Function {twitter_tweet_replies.__name__} -> {e}")
        return False, None, f"Error obtaining all tweet's (id:{tweet_id}) replies"


def twitter_search_tweets(tweet):
    """
    Args:
        tweet_id: Tweet's ID

    Return: Search tweet that starts with the id
    """
    try:
        tweets = Tweet.objects.filter(Q(tweet_id__startswith=tweet))

        data = [serializers.Tweet(tweet).data["tweet_id"] for tweet in tweets]

        return True, data, f"Success searching users by {tweet}"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_search_tweets.__name__} -> {e}")
        return False, None, f"Error searching users by {tweet}"


def twitter_strict_search(keyword):
    """
    Args:
        keyword: The keyword with which we want to look up the user

    Return: Data with entities that have that keyword
    """
    try:
        data = {"User": [], "Bot": [], "Tweet": []}
        if keyword.isdigit():
            tweets = Tweet.objects.filter(Q(tweet_id__startswith=keyword))
            data["Tweet"] = [serializers.Tweet(tweet).data["tweet_id"] for tweet in tweets]

        bot_query = Q()
        print(len(bot_query))
        for bot in neo4j.search_bots():
            if bot["username"].lower().startswith(keyword.lower()):
                bot_query |= Q(user_id=bot["id"])

        if len(bot_query) > 0:
            bots = User.objects.filter(bot_query)
            bots_serializer = [serializers.User(bot).data for bot in bots]
            data["Bot"] = [{
                "id": bot["user_id"], "screen_name": bot["screen_name"], "name": bot["name"]
            } for bot in bots_serializer]

        users = User.objects.filter(Q(screen_name__istartswith=keyword)).exclude(bot_query)
        users_serializer = [serializers.User(user).data for user in users]
        data["User"] = [{
            "id": user["user_id"], "screen_name": user["screen_name"], "name": user["name"]
        } for user in users_serializer]

        return True, data, f"Success searching entities by {keyword}"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_strict_search.__name__} -> {e}")
        return False, None, f"Error searching users by {keyword}"


# -----------------------------------------------------------
# policies
# -----------------------------------------------------------

def policy(policy_id):
    """

    Args:
        policy_id:  Policy's ID

    Returns: Policy's info  wrapped on  dictionary

    """
    try:
        policy_by_id = Policy.objects.get(id=policy_id)
        return True, serializers.Policy(policy_by_id).data, f"Success obtaining policy's (id:{policy_id}) info"

    except Policy.DoesNotExist as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy.__name__} -> {e}")
        return False, None, f"Policy (id:{policy_id}) does not exist on database"
    except Exception as e:

        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policy.__name__} -> {e}")
        return False, None, f"Error obtaining policy's (id:{policy_id}) info"


def policies(entries_per_page, page):
    """

    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All policies saved wrapped on dictionary divided in pages
    if entries_per_page and page are both None then all policies will be returned
    """
    try:
        all_policies = Policy.objects.all()

        data = paginator_factory(all_policies, entries_per_page, page)
        data['entries'] = [serializers.Policy(policy_obj).data for policy_obj in data['entries']]
        for entry in data['entries']:
            for index in range(len(entry['bots'])):
                bot_id = entry['bots'][index]
                user_obj = User.objects.filter(user_id=bot_id)
                bot_name = user_obj[0].screen_name if len(user_obj) > 0 else ''
                entry['bots'][index] = {"bot_id": bot_id, "bot_name": bot_name}

        return True, data, "Success obtaining all policies"
    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policies.__name__} -> {e}")
        return False, None, "Error obtaining all policies"


def bot_policies(bot_id, entries_per_page, page):
    """

    Args:
        bot_id: Bot's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: Bot assigned policies wrapped on dictionary divided in pages
    if entries_per_page and page are both None then all bots will be returned
    """
    try:
        policies_list = Policy.objects.filter(bots__contains=[bot_id])

        data = paginator_factory(policies_list, entries_per_page, page)
        data['entries'] = [serializers.Policy(policy_obj).data for policy_obj in data['entries']]

        return True, data, f"Success obtaining bot's (id:{bot_id}) policy info"
    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {bot_policies.__name__} -> {e}")
        return False, None, f"Error obtaining bot's (id:{bot_id}) policy info"


def get_number_policies():
    """
    Returns: Dictionary with total number of policies, and number of active policies
    """
    try:
        data = {"total": Policy.objects.all().count(), "active": Policy.objects.filter(active=True).count()}
        return True, data, "Success obtaining all policies"
    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {policies.__name__} -> {e}")
        return False, None, "Error obtaining all policies"


def add_policy(data):
    """
    Add new policy to DB
    :param data: Dictionary with data to be inserted
        Items:
            - id : int
            - API_type : str
            - filter : str
            - name : str
            - tags : str[]
            - bots : int[]
        Ex: { "API_type": "Twitter", "filter": "Instagram", "name": "Politica", "tags": ["PSD", "CDS"], "bots": [1, 2] }
    :return: status(boolean), data, message(string)
    """

    class AddPolicyError(Exception):
        pass

    try:
        policy_serializer = serializers.Policy(data=data)
        if not policy_serializer.is_valid():
            return False, policy_serializer.errors, "Invalid data"

        for bot_id in policy_serializer.data['bots']:
            if not neo4j.check_bot_exists(str(bot_id)):
                raise AddPolicyError("Invalid Bot's ID")

            if Policy.objects.filter(name=policy_serializer.data['name']).exists():
                raise AddPolicyError("A policy with same name already exists")

            if Policy.objects.filter(Q(tags__overlap=policy_serializer.data['tags'])).exists():
                raise AddPolicyError(
                    "Some of the policy arguments are already defined in another policy. Tags cant overlap!")

        data = policy_serializer.data
        data['tags'] = list(set(data['tags']))

        policy = Policy.objects.create(id=next_id(Policy), **data)

        return True, {'id': policy.id}, "Success adding a new policy"

    except AddPolicyError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
        return False, None, str(e)
    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_policy.__name__} -> {e}")
        return False, None, "Error adding a new policy"


def remove_policy(policy_id):
    """

    Args:
        policy_id:  Policy's ID

    Returns: Remove operation status wrapped on dictionary

    """
    try:
        Policy.objects.get(id=policy_id).delete()
        return True, None, f"Successful policy  (id:{policy_id}) removal"

    except Policy.DoesNotExist:
        return False, None, f"Policy (id:{policy_id}) does not exist on database"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {remove_policy.__name__} -> {e}")
        return False, None, f"Error policy  (id:{policy_id}) removal"


def update_policy(data, policy_id):
    """

    Args:
        data: Dictionary with data to be updated
        policy_id: Policy's ID

    Returns: Update operation status wrapped on dictionary

    """

    class UpdatePolicyError(Exception):
        pass

    try:
        policy_obj = Policy.objects.get(id=policy_id)
        data = dict([(key, value) for key, value in data.items() if key != 'id'])
        if 'tags' in data:
            data['tags'] = list(set(data['tags']))
        policy_obj.__dict__.update(data)

        new_data = serializers.Policy(policy_obj).data
        for bot_id in new_data['bots']:
            if not neo4j.check_bot_exists(str(bot_id)):
                raise UpdatePolicyError("Invalid Bot's ID")

        if Policy.objects.filter(Q(name=new_data['name']) & ~Q(id=policy_id)).exists():
            raise UpdatePolicyError("A policy with same name already exists")

        if Policy.objects.filter(Q(tags__overlap=new_data['tags']) & ~Q(id=policy_id)).exists():
            raise UpdatePolicyError(
                "Some of the policy arguments are already defined in another policy. Tags cant overlap!")

        policy_obj.save()

        entry = serializers.Policy(policy_obj).data

        for index in range(len(entry['bots'])):
            bot_id = entry['bots'][index]
            user_obj = User.objects.filter(user_id=bot_id)
            bot_name = user_obj[0].screen_name if len(user_obj) > 0 else ''
            entry['bots'][index] = {"bot_id": bot_id, "bot_name": bot_name}

        return True, entry, f"Success in updating the policy (id:{policy_id})"

    except Policy.DoesNotExist as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
        return False, None, f"Policy (id:{policy_id}) does not exists on database"

    except UpdatePolicyError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {update_policy.__name__} -> {e}")
        return False, None, f"Error in updating the policy (id:{policy_id})"


# Bots
def twitter_bot_logs(bot_id, entries_per_page, page):
    """

    Args:
        bot_id: Bots's ID
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns:  Bot's logs wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all logs will be returned

    """
    try:
        logs = Log.objects.filter(id_bot=bot_id).order_by('-timestamp')

        data = paginator_factory(logs, entries_per_page, page)
        data['entries'] = [serializers.Log(log).data for log in data['entries']]

        for entry in data['entries']:
            target_id = entry['target_id']
            user_obj = User.objects.filter(user_id=target_id)
            entry['target_screen_name'] = user_obj[0].screen_name if len(user_obj) > 0 else ''

        return True, data, f"Success obtaining bot's (id:{bot_id}) logs"

    except ValueError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_logs.__name__} ->  {e}")
        return False, None, f"Error obtaining bot's (id:{bot_id}) logs"


def twitter_bot(bot_id):
    """

    Args:
        bot_id: Bot's ID

    Returns: Bot's info wrapped on dictionary

    """
    try:
        if not neo4j.check_bot_exists(bot_id):
            return False, None, f"Bot (id:{bot_id}) does not exist on database"

        return True, serializers.User(User.objects.get(user_id=int(bot_id))).data, \
               f"Success obtaining bot's (id:{bot_id}) info"

    except User.DoesNotExist as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot.__name__} -> {e}")
        return False, None, f"Bot (id:{bot_id}) does not exist on both database"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot.__name__} -> {e}")
        return False, None, f"Error obtaining bot's (id:{bot_id}) info"


def twitter_bots():
    """

    Returns: All bots's info saved on database wrapped on dictionary

    """
    try:
        bots_ids = [int(bot['id']) for bot in neo4j.search_bots()]

        data = [serializers.User(user).data for user in User.objects.filter(user_id__in=bots_ids)]

        return True, data, "Success obtaining bots's info"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bots.__name__} -> {e}")
        return False, None, "Error obtaining bots's info"


def twitter_bot_messages(bot_id):
    """

    Args:
        bot_id: Bots'ID

    Returns:

    """
    try:
        data = [serializers.Message(msg).data for msg in Message.objects.filter(bot_id=bot_id)]
        return True, data, f"Success obtaining bot's (id:{bot_id}) direct messages"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_bot_messages.__name__} -> {e}")
        return False, None, f"Error obtaining bot's (id:{bot_id}) direct messages"


# Network
def twitter_sub_network(request):
    """

    Args:
        queries:  Array of neo4j queries

    Returns: Neo4'j sub network in json format wrapped on response's object

    """
    try:
        match = {
            "start": request["start"],
            "intermediates": request["intermediate"],
            "end": request["end"]
        }
        if "limit" not in request or not request["limit"]:
            request["limit"] = 1000

        protected = 'u_protected_only' in request['fields']['User']
        print(request)

        data = neo4j.export_query(Report.neo_query_builder(match, request["limit"], protected))
        return True, [process_neo4j_results(data)], \
               "Success obtaining a network defined by a query"

    except AttributeError as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
        return False, None, str(e)

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_sub_network.__name__} -> {e}")
        return False, None, "Error obtaining a network defined by a query"


def twitter_network():
    """

    Returns:  Neo4'j network in json format wrapped on dictionary

    """

    try:
        data = neo4j.export_query(NETWORK_QUERY)

        return True, [process_neo4j_results(data)], f"Success obtaining full network"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {twitter_network.__name__} -> {e}")
        return False, None, f"Error obtaining full network"


@cache(cacheAPI, model_name="neo4j", pagination=True)
def entities_counter():
    """

    Returns: Entities counter (bots,users,tweets) info saved on database wrapped on dictionary

    """
    try:
        data = neo4j.get_entities_stats()
        return True, dict(list(data)), f"Success obtaining entities counter"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {entities_counter.__name__} -> {e}")
        return False, None, f"Error obtaining entities counter"


@cache(cacheAPI, "Tweet", pagination=True)
def latest_tweets(counter, entries_per_page, page):
    """

    Args:
        counter: Number of tweets to return
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: Latest tweets wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all latest tweets  will be returned
    """
    try:
        tweets = Tweet.objects.all().order_by("-created_at")[:counter].values()

        data = paginator_factory_non_queryset(tweets, entries_per_page, page)
        data['entries'] = [serializers.Tweet(tweet).data for tweet in data['entries']]

        return True, data, f"Success obtaining latest tweets"

    except Exception as e:
        logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {latest_tweets.__name__} -> {e}")
        return False, None, f"Error obtaining latest tweets"


@cache(cacheAPI, model_name="Log", pagination=True)
def latest_activities_daily(entries_per_page, page):
    """
    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All bots's daily activities wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all bots's daily activities  will be returned

    """
    try:
        activities = Log.objects.filter(Q(timestamp__gte=datetime.now() - timedelta(days=1))
                                        & Q(timestamp__lte=datetime.now())).order_by("-timestamp")

        data = paginator_factory(activities, entries_per_page, page)
        data['entries'] = [serializers.Log(activity).data for activity in data['entries']]

        for entry in data['entries']:
            user = User.objects.filter(user_id=int(entry['id_bot']))
            screen_name = ''
            if user.count() >= 1:
                screen_name = user[0].screen_name

            entry['bot_screen_name'] = screen_name
            user_obj = User.objects.filter(user_id=int(entry['target_id']))
            entry['target_screen_name'] = user_obj[0].screen_name if len(user_obj) > 0 else ''

        return True, data, "Success obtaining latest bot's activities daily"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {latest_activities_daily.__name__} -> {e}")
        return False, None, "Error obtaining latest bot's activities daily"


@cache(cacheAPI, model_name="Log", pagination=True)
def latest_activities(counter, entries_per_page, page):
    """
    Args:
        counter: Number of tweets to return
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All bots's activities limited by counter wrapped on dictionary divided by pages
    if entries_per_page and page are both None then aAll bots's activities limited by counter will be returned

    """
    try:
        activities = Log.objects.all().order_by("-timestamp")[:counter]

        data = paginator_factory(activities, entries_per_page, page)
        data['entries'] = [serializers.Log(activity).data for activity in data['entries']]

        for entry in data['entries']:
            bot_screen_name = ''
            bot = User.objects.filter(user_id=int(entry['id_bot']))
            if bot.count() > 0:
                bot_screen_name = bot[0].screen_name
            entry['bot_screen_name'] = bot_screen_name
            user_obj = User.objects.filter(user_id=int(entry['target_id']))
            entry['target_screen_name'] = user_obj[0].screen_name if len(user_obj) > 0 else ''

        return True, data, "Success obtaining latest bot's activities"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {latest_activities.__name__} -> {e}")
        return False, None, "Error obtaining latest bot's activities"


def __get_count_stats(types, accum, last_id, action):
    query = "Log.objects"
    if action:
        query += f".filter(action='{action}')"

    if last_id is not None:
        query += f".filter(id__gt={last_id})"

    for group_type in types:
        query += f".annotate({group_type}=Extract{group_type.title()}('timestamp'))"

    order_by_list = [f"'{group_type}'" for group_type in types]
    query += f".values({','.join(order_by_list)})" \
             f".annotate(activity=Count('*'))" \
             f".order_by({','.join(order_by_list)})"

    stats = {'entries': {}, 'last_id': Log.objects.aggregate(Max('id'))['id__max']}

    query_res = list(eval(query))

    for index in range(len(query_res)):
        obj = query_res[index]
        if index > 0 and accum:
            obj['activity'] += query_res[index - 1]['activity']
        full_date = '/'.join(str(obj.pop(group_type)) for group_type in types)
        stats['entries'][full_date] = obj['activity']

    return stats


def __get_today_stats(action=None):
    query = "Log.objects.filter(Q(timestamp__gte=datetime.now() - timedelta(days=1))" \
            "& Q(timestamp__lte=datetime.now())"
    if action:
        query += f" & Q(action='{action}')"

    query += ").count()"

    return eval(query)


@cache(cacheAPI, model_name="Log", pagination=False)
def gen_stats_grouped(types, accum=False, last_id=None):
    """
    Args:
        types: Group labels (day,month,year)

    Returns: User's stats  grouped by (day or month or year) wrapped on dictionary

    """
    try:
        gen_stats = __get_count_stats(types, accum, last_id['gen'] if last_id else None, None)

        data = {'entries': [], 'last_id': {
            'gen': gen_stats['last_id']
        }}
        for date in gen_stats['entries']:
            stats = {'general': gen_stats['entries'][date], 'date': date}

            data['entries'].append(stats)
        return True, data, f"Success obtaining stats grouped"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {gen_stats_grouped.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="Log", pagination=False)
def user_tweets_stats_grouped(types, accum=False, last_id=None):
    try:
        user_stats = __get_count_stats(types, accum, last_id['user'] if last_id else None, action='INSERT USER')

        tweet_stats = __get_count_stats(types, accum, last_id['tweet'] if last_id else None, action='INSERT TWEET')

        data = {'entries': [], 'last_id': {
            'user': user_stats['last_id'],
            'tweet': tweet_stats['last_id']
        }}

        for date in user_stats['entries']:
            stats = {'date': date, 'users': user_stats['entries'][date], 'tweets': 0}
            if len(data['entries']) > 0 and accum:
                stats['tweets'] = data['entries'][-1]['tweets']

            if date in tweet_stats['entries']:
                stats['tweets'] = tweet_stats['entries'][date]
            data['entries'].append(stats)

        return True, data, f"Success obtaining stats grouped"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {user_tweets_stats_grouped.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="Log", pagination=False)
def relations_stats_grouped(types, accum=False, last_id=None):
    try:
        follow_stats = __get_count_stats(types, accum, last_id['follow'] if last_id else None, action='FOLLOW')

        like_stats = __get_count_stats(types, accum, last_id['like'] if last_id else None, action="TWEET LIKE")

        reply_stats = __get_count_stats(types, accum, last_id['reply'] if last_id else None, action="TWEET REPLY")

        retweet_stats = __get_count_stats(types, accum, last_id['retweet'] if last_id else None, action="RETWEET")

        quote_stats = __get_count_stats(types, accum, last_id['quote'] if last_id else None, action="TWEET QUOTE")

        data = {
            'entries': [],
            'last_id': {
                'follow': follow_stats['last_id'],
                'like': like_stats['last_id'],
                'reply': reply_stats['last_id'],
                'retweet': retweet_stats['last_id'],
                'quote': quote_stats['last_id']
            }
        }
        for date in follow_stats['entries']:
            stats = {'date': date, 'follows': follow_stats['entries'][date], 'likes': 0, 'replies': 0, 'retweets': 0,
                     'quote': 0}

            if len(data['entries']) > 0 and accum:
                stats['likes'] = data['entries'][-1]['likes']
                stats['replies'] = data['entries'][-1]['replies']
                stats['retweets'] = data['entries'][-1]['retweets']
                stats['quote'] = data['entries'][-1]['quote']

            if date in like_stats['entries']:
                stats['likes'] = like_stats['entries'][date]
            if date in reply_stats['entries']:
                stats['replies'] = reply_stats['entries'][date]
            if date in retweet_stats['entries']:
                stats['retweets'] = retweet_stats['entries'][date]
            if date in quote_stats['entries']:
                stats['quote'] = quote_stats['entries'][date]

            data['entries'].append(stats)

        return True, data, f"Success obtaining stats grouped"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {relations_stats_grouped.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


def rafa_is_lindo():
    """
    Most important function in this module

    Returns: Most important message in this module
    """

    try:
        return True, "Rafa é lindo", "Success obtaining stats grouped"
    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {rafa_is_lindo.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="Log", pagination=True)
def general_today():
    """
    Returns: number of activities the bots had today
    """
    try:
        return True, {"data": __get_today_stats()}, "Success obtaining stats grouped"
    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {general_today.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="Log", pagination=True)
def user_tweets_today():
    """
    Returns: number of users and tweets the bot found today
    """
    try:
        data = {"user": __get_today_stats("INSERT USER"), "tweets": __get_today_stats("INSERT TWEET")}
        return True, data, "Success obtaining stats grouped"
    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {user_tweets_today.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="Log", pagination=True)
def relations_today():
    """
    Returns: number of relations betweens entities the bot found today
    """
    try:
        data = {"follow": __get_today_stats("FOLLOW"), "likes": __get_today_stats("TWEET LIKE"),
                "retweet": __get_today_stats("RETWEET"), "quotes": __get_today_stats("TWEET QUOTE"),
                "replies": __get_today_stats("REPLIES")}
        return True, data, "Success obtaining stats grouped"
    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {relations_today.__name__} -> {e}")
        return False, None, f"Error obtaining stats grouped"


@cache(cacheAPI, model_name="TweetStats", pagination=True)
def latest_tweets_daily(entries_per_page, page):
    """
    Args:
        entries_per_page: Number of entries per page or None
        page: Number of page the user wants to retrieve or None

    Returns: All bots's daily tweets wrapped on dictionary divided by pages
    if entries_per_page and page are both None then all bots's daily activities  will be returned

    """
    try:
        tweets = TweetStats.objects.filter(Q(timestamp__gte=datetime.now() - timedelta(days=1))
                                           & Q(timestamp__lte=datetime.now())).order_by("-timestamp")

        data = paginator_factory(tweets, entries_per_page, page)
        tweet_list = [serializers.TweetStats(tweet).data for tweet in data['entries']]
        serialized_entries = []

        for tweet in tweet_list:
            entry = Tweet.objects.filter(tweet_id=tweet["tweet_id"])
            if entry.count() == 0:
                kwargs = {
                    "tweet_id": str(tweet['tweet_id']),
                    "user": {
                        "id": tweet['user_id'],
                        "id_str": str(tweet['user_id'])
                    }
                }
                entry = [Tweet(**kwargs)]
            serialized_entries.append(serializers.Tweet(entry[0]).data)

        data['entries'] = serialized_entries

        return True, data, "Success obtaining latest bot's tweets daily"

    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {latest_tweets_daily.__name__} -> {e}")
        return False, None, "Error obtaining latest bot's tweets daily"


def add_emails(data):
    """
    :param data: Dictionary with data to be inserted
    Returns: Add operation status wrapped on dictionary
    """
    try:
        n_data = serializers.Notification(data=data)
        if not n_data.is_valid():
            return False, n_data.errors

        if not Notification.objects.filter(email=n_data.data['email']).exists():
            Notification.objects.create(email=n_data.data['email'], status=n_data.data['status'])
        else:
            Notification.objects.filter(email=n_data.data['email']).update(status=True)

        return True, "Success adding a new email"
    except Exception as e:
        logger.error(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Function {add_emails.__name__} -> {e}")
        return False, "Error adding a new email"
