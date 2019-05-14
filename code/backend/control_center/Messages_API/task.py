from mongo_api import MongoAPI
from postgreSQL import postgreSQL_API
from send import RabbitSend
from policy_api import PolicyAPI
from neo4j_api import Neo4jAPI
from enums import MessageTypes, Neo4jTypes, PoliciesTypes

class Task():
    def __init__(self):
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.neo4j = Neo4jAPI()
        self.policy = PolicyAPI()
        self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')


    def menu(self, message_type, message):
        if (message_type == MessageTypes.USER_FOLLOWED):
            pass
        elif (message_type == MessageTypes.TWEET_LIKED):
            pass
        elif (message_type == MessageTypes.TWEET_RETWEETDED):
            pass
        elif (message_type == MessageTypes.TWEET_REPLIED):
            pass
        elif (message_type == MessageTypes.REQUEST_TWEET_LIKE):
            print("TASK: REQUEST LIKE TWEET")
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_LIKE,
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            #Routing Key
            r_key = 'tasks.deliver.'+message['bot_id']
            #Message
            msm = {"type": 3, "response": result}
            self.rabbit.send(routing_key=r_key,message=msm)

        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            print("TASK: REQUEST RETWEET TWEET")
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_RETWEET,
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            #Routing Key
            r_key = 'tasks.deliver.'+message['bot_id']
            #Message
            msm = {"type": 4,"response": result}
            self.rabbit.send(routing_key=r_key,message=msm)

        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            print("TASK: REQUEST REPLY TWEET")
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_REPLY,
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities'],
                "tweet_in_reply_to_status_id_str": message['data']['in_reply_to_status_id_str'],
                "tweet_in_reply_to_user_id_str": message['data']['in_reply_to_user_id_str'],
                "tweet_in_reply_to_screen_name": message['data']['in_reply_to_screen_name']
            }
            result = self.policy.lifecycle(data)
            #Routing Key
            r_key = 'tasks.deliver.'+message['bot_id']
            #Message
            msm = {"type": 5,"response": result}
            self.rabbit.send(routing_key=r_key,message=msm)

        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            print("TASK: REQUEST FOLLOW USER")
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_REPLY,
                "bot_id": message['bot_id'],
                "user_id": message['data']['id'],
            }
            result = self.policy.lifecycle(data)
            """ #Search if User is already Followed by another Bot
            result = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"user_id": message['data']['id']}) """
            #Routing Key
            r_key = 'tasks.deliver.'+message['bot_id']
            #Message
            msm = {"type": 1,"response": result}
            self.rabbit.send(routing_key=r_key,message=msm)

        elif(message_type == MessageTypes.SAVE_USER):
            print("TASK: SAVE USER")
            is_bot = False
            if (message['bot_id']==message['data']['id']):
                is_bot = True
            if (is_bot):
                #Asks Neo4j if Bot exists
                exists = self.neo4j.task(Neo4jTypes.SEARCH_BOT,data={"bot_id": message['bot_id']})
                if (exists):
                    #Update User in Mongo Database
                    self.mongo.update('users', message['data'])
                    #Update User in NEO4J Database
                    self.neo4j.task(Neo4jTypes.UPDATE_BOT,data={"bot_id": message['bot_id'], "bot_name": message['data']['name'], "bot_username": message['data']['screen_name']})
                else:
                    #Save User in Mongo Database
                    self.mongo.save('users', message['data'])
                    #Create User in Neo4j
                    self.neo4j.task(Neo4jTypes.CREATE_BOT,data={"id": message['bot_id'], "name": message['data']['name'], "username": message['data']['screen_name']})
            else:
                #Asks Neo4j if User exists
                exists = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"user_id": message['data']['id']})
                if (exists):
                    #Update User in Mongo Database
                    self.mongo.update('users', message['data'])
                    #Update User in NEO4J Database
                    self.neo4j.task(Neo4jTypes.UPDATE_USER,data={"user_id": message['data']['id'], "user_name": message['data']['name'], "user_username": message['data']['screen_name']})
                else:
                    #Save User in Mongo Database
                    self.mongo.save('users', message['data'])
                    #Create User in Neo4j
                    self.neo4j.task(Neo4jTypes.CREATE_USER,data={"id": message['data']['id'], "name": message['data']['name'], "username": message['data']['screen_name']})
                    #Create Relation between Bot and User
                    self.neo4j.task(Neo4jTypes.CREATE_RELATION,data={"bot_id": message['bot_id'], "user_id": message['data']['id']})

            
            #TODO: Postgres for Users

        elif(message_type == MessageTypes.SAVE_TWEET):
            print("TASK: SAVE TWEET")            
            self.mongo.save('tweets', message['data'])
            self.postgreSQL.insertDataTweets(message['data']['timestamp'],message['data']['id'],message['data']['user_id'],message['data']['likes_count'],message['data']['retweets_count'])

        elif(message_type == MessageTypes.SAVE_TWEET):
            print("TASK: ERROR_BOT")            
            return message