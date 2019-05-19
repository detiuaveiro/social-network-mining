from Mongo.mongo_api import MongoAPI
from Postgres.postgreSQL import postgreSQL_API
from send import RabbitSend
from policy_api import PolicyAPI
from Neo4j.neo4j_api import Neo4jAPI
from Enums.enums import MessageTypes, Neo4jTypes, PoliciesTypes, ResponseTypes

class Task():
    def __init__(self):
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.postgreSQL2 = postgreSQL_API("policies")
        self.neo4j = Neo4jAPI()
        self.policy = PolicyAPI()


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
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO LIKE TWEET (ID: "+str(message['data']['id'])+" )"})
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_LIKE,
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            if (result==1):
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE LIKED"})
                #Routing Key
                r_key = 'tasks.twitter.'+message['bot_id']
                #Message
                msm = {"type": ResponseTypes.LIKE_TWEETS, "params": message['data']['id']}
                try:
                    self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                    self.rabbit.send(routing_key=r_key,message=msm)
                    self.rabbit.close()
                except:
                    print("WARNING: FAILED TO SEND")
            else:
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE LIKED"})

        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            print("TASK: REQUEST RETWEET TWEET")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO RETWEET TWEET (ID: "+str(message['data']['id'])+" )"})
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_RETWEET,
                "bot_id": message['bot_id'],
                "tweet_id": message['data']['id'],
                "tweet_text": message['data']['text'],
                "tweet_entities": message['data']['entities']
            }
            result = self.policy.lifecycle(data)
            if (result==1):
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE RETWEETED"})
                #Routing Key
                r_key = 'tasks.twitter.'+message['bot_id']
                #Message
                msm = {"type": ResponseTypes.RETWEET_TWEETS,"params": message['data']['id']}
                try:
                    self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                    self.rabbit.send(routing_key=r_key,message=msm)
                    self.rabbit.close()
                except:
                    print("WARNING: FAILED TO SEND")
            else:
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE RETWEETED"})


        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            print("TASK: REQUEST REPLY TWEET")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO REPLY TWEET (ID: "+str(message['data']['id'])+" )"})
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
            if (result==1):
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE REPLIED"})
                #Routing Key
                r_key = 'tasks.twitter.'+message['bot_id']
                #Message
                msm = {"type": ResponseTypes.REPLY_TWEETS,"params": message['data']['id']}
                try:
                    self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                    self.rabbit.send(routing_key=r_key,message=msm)
                    self.rabbit.close()
                except:
                    print("WARNING: FAILED TO SEND")
            else:
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE REPLIED"})


        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            print("TASK: REQUEST FOLLOW USER")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO FOLLOW USER ("+str(message['data']['id'])+")"})
            data = {
                "type": PoliciesTypes.REQUEST_TWEET_REPLY,
                "bot_id": message['bot_id'],
                "user_id": message['data']['id'],
            }
            result = self.policy.lifecycle(data)
            if (result==1):
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "USER (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE FOLLOWED"})
                #Routing Key
                r_key = 'tasks.twitter.'+message['bot_id']
                #Message
                msm = {"type": ResponseTypes.FOLLOW_USERS,"params": {"type": "id", "data": [message['data']['id']]}}
                try:
                    self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                    self.rabbit.send(routing_key=r_key,message=msm)
                    self.rabbit.close()
                except:
                    print("WARNING: FAILED TO SEND")
            else:
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "USER (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE FOLLOWED"})

            """ #Search if User is already Followed by another Bot
            result = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"user_id": message['data']['id']}) """


        elif(message_type == MessageTypes.SAVE_USER):
            print("TASK: SAVE USER")
            is_bot = False
            if (int(message['bot_id'])==message['data']['id']):
                print("INFO: USER IS BOT")
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
                    data = {
                        "type": PoliciesTypes.FIRST_TIME,
                        "bot_id": message['bot_id'],
                    }
                    result = self.policy.lifecycle(data)
                    #Routing Key
                    r_key = 'tasks.twitter.'+message['bot_id']
                    #Message
                    print(result)
                    msm = {"type": ResponseTypes.FOLLOW_USERS,"params": {"type": "screen_name", "data": result}}
                    try:
                        self.rabbit = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                        self.rabbit.send(routing_key=r_key,message=msm)
                        self.rabbit.close()
                    except:
                        print("WARNING: FAILED TO SEND")
                    #Save User in Mongo Database
                    self.mongo.save('users', message['data'])
                    #Create User in Neo4j
                    self.neo4j.task(Neo4jTypes.CREATE_BOT,data={"id": message['bot_id'], "name": message['data']['name'], "username": message['data']['screen_name']})
            else:
                #Asks Neo4j if User exists
                exists = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"user_id": message['data']['id']})
                if (exists):
                    self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "UPDATING USER INFO ("+str(message['data']['id'])+")"})
                    #Update User in Mongo Database
                    self.mongo.update('users', message['data'])
                    #Update User in NEO4J Database
                    self.neo4j.task(Neo4jTypes.UPDATE_USER,data={"user_id": message['data']['id'], "user_name": message['data']['name'], "user_username": message['data']['screen_name']})
                else:
                    self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "SAVING NEW USER ("+str(message['data']['id'])+")"})
                    #Save User in Mongo Database
                    self.mongo.save('users', message['data'])
                    #Create User in Neo4j
                    self.neo4j.task(Neo4jTypes.CREATE_USER,data={"id": message['data']['id'], "name": message['data']['name'], "username": message['data']['screen_name']})
                    #Create Relation between Bot and User
                    self.neo4j.task(Neo4jTypes.CREATE_RELATION,data={"bot_id": message['bot_id'], "user_id": message['data']['id']})

            self.postgreSQL.addUser(mapa={"user_id": message['data']['id'], "followers": message['data']['followers_count'], "following": message['data']['friends_count']})

        elif(message_type == MessageTypes.SAVE_TWEET):
            print("TASK: SAVE TWEET")
            #Check if tweet exists
            tweet_exists = self.mongo.search('tweets', message['data'])
            if (tweet_exists):
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "UPDATING TWEET STATS ("+str(message['data']['id'])+")"})
                self.mongo.update('tweets', message['data'])
            else:
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "SAVING TWEET ("+str(message['data']['id'])+")"})
                self.mongo.save('tweets', message['data'])
            self.postgreSQL.addTweet(mapa={"tweet_id": message['data']['timestamp'], "user_id": message['data']['id'], "likes": message['data']['likes_count'], "retweets": message['data']['retweets_count']})

        elif(message_type == MessageTypes.SAVE_TWEET):
            print("TASK: ERROR_BOT")           
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "WARNING: BOT WITH THE FOLLOWING ID "+str(message['bot_id'])+" GAVE THIS ERROR "+str(message['data']['msm'])})