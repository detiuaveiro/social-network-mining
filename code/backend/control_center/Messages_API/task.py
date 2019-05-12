from mongo_api import MongoAPI
from postgreSQL import postgreSQL_API
from policy_api import PolicyAPI
from neo4j_api import Neo4jAPI
from rabbitmq import Rabbitmq
from enums import MessageTypes, Neo4jTypes

class Task():
    def __init__(self):
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.policy = PolicyAPI()
        self.rabbit = Rabbitmq(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')


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
            print('Received a request to like tweet')
            data = {
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            r_key = 'tasks.deliver.'+message['bot_id']
            m = {"message_type": 2,"response": result}
            self.rabbit.send(exchange='task_deliver',routing_key=r_key,message=m)
        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            print('Received a request to retweet a tweet')
            data = {
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            r_key = 'tasks.deliver.'+message['bot_id']
            m = {"message_type": 2,"response": result}
            self.rabbit.send(exchange='task_deliver',routing_key=r_key,message=m)

        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            print('Received a request to reply to a tweet')
            data = {
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities'],
                "tweet_in_reply_to_status_id_str": message['data']['in_reply_to_status_id_str'],
                "tweet_in_reply_to_user_id_str": message['data']['in_reply_to_user_id_str'],
                "tweet_in_reply_to_screen_name": message['data']['in_reply_to_screen_name']
            }
            result = self.policy.lifecycle(data)
            r_key = 'tasks.deliver.'+message['bot_id']
            m = {"message_type": 2,"response": result}
            self.rabbit.send(exchange='task_deliver',routing_key=r_key,message=m)

        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            print('Received a request to follow user')
            data = {
                "tweet_user_id": message['data']['id'],
            }
            self.neo4j = Neo4jAPI()
            result = self.neo4j.task(Neo4jTypes.SEARCH_USER,data)
            self.neo4j.close()
            r_key = 'tasks.deliver.'+message['bot_id']
            m = {"message_type": 2,"response": result}
            self.rabbit.send(exchange='task_deliver',routing_key=r_key,message=m)

        elif(message_type == MessageTypes.SAVE_USER):
            print('An User is being saved')

            self.mongo.save('users', message['data'])
            self.neo4j = Neo4jAPI()
            result = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"tweet_user_id": message['data']['id']})
            #IF BOT EXISTS DO THIS
            if (result==1):
                self.neo4j.task(Neo4jTypes.UPDATE_USER,data={"user_id": message['data']['id'], "user_name": message['data']['name'], "user_username": message['data']['username']})
            else:
                self.neo4j.task(Neo4jTypes.CREATE_USER,data={"id": message['data']['id'], "name": message['data']['name'], "username": message['data']['username']})
                self.neo4j.task(Neo4jTypes.CREATE_RELATION,data={"bot_id": message['data']['bot_id'], "user_id": message['data']['user_id']})
            
            self.neo4j.close()


        elif(message_type == MessageTypes.SAVE_TWEET):
            print('A Tweet is being saved')
            self.mongo.save('tweets', message['data'])
            self.postgreSQL.insertDataTweets(message['data']['timestamp'],message['data']['id'],message['data']['user_id'],message['data']['likes_count'],message['data']['retweets_count'])
