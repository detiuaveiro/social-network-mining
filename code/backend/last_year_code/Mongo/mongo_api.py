from pymongo import MongoClient
import logging
import sys
import settings

log = logging.getLogger('Mongo')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

### Mongo API
# Class used to establish connection to a Mongo Server
# Does all basic CRUD methods
class MongoAPI():
    def __init__(self):
        log.debug("Connecting to MongoDB")
        self.client = MongoClient('mongodb://'+settings.MONGO_FULL_URL)
        self.users = self.client.twitter.users
        self.tweets = self.client.twitter.tweets
        self.messages = self.client.twitter.messages

    def save(self, database, data):
        self.database = database
        self.data = data

        if (self.database=='users'):
            try:
                self.users.insert_one(self.data)
            except:
                log.info("ERROR INSERTING USER")
        elif (self.database=='messages'):
            try:
                self.messages.insert_one(self.data)
            except:
                log.info("ERROR INSERTING MESSAGE")
        elif (self.database=='tweets'):
            try:
                self.tweets.insert_one(self.data)
            except:
                log.info("ERROR INSERTING TWEET")

    def update(self, database, data):
        self.database = database
        self.data = data
        if (self.database=='users'):
            try:
                self.users.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                log.info("ERROR UPDATING USER ("+str(e)+")")
        elif (self.database=='messages'):
            try:
                self.messages.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                log.info("ERROR UPDATING MESSAGE ("+str(e)+")")
        elif (self.database=='tweets'):
            try:
                self.tweets.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                log.info("ERROR UPDATING TWEET ("+str(e)+")")

    def search(self, database, data):
        self.database = database
        self.data = data
        if (self.database=='users'):
            try:
                result = self.users.find_one({"id": self.data['id']})
                if(result):
                    return True
                else:
                    return False
            except:
                log.info("ERROR SEARCHING FOR USER")
        elif (self.database=='messages'):
            try:
                result = self.messages.find_one({"id": self.data['id']})
                if(result):
                    return True
                else:
                    return False
            except:
                log.info("ERROR SEARCHING FOR MESSAGE")
        elif (self.database=='tweets'):
            try:
                result = self.tweets.find_one({"id": self.data['id']})
                if(result):
                    return True
                else:
                    return False
            except Exception as e:
                log.info("ERROR SEARCHING FOR TWEET: "+str(e))