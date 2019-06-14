from pymongo import MongoClient

import settings

class MongoAPI():
    def __init__(self):
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
                print("ERROR INSERTING USER")
        if (self.database=='messages'):
            try:
                self.messages.insert_one(self.data)
            except:
                print("ERROR INSERTING MESSAGE")
        else:
            try:
                self.tweets.insert_one(self.data)
            except:
                print("ERROR INSERTING TWEET")

    def update(self, database, data):
        self.database = database
        self.data = data
        if (self.database=='users'):
            try:
                self.users.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                print("ERROR UPDATING USER ("+str(e)+")")
        if (self.database=='messages'):
            try:
                self.messages.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                print("ERROR UPDATING MESSAGE ("+str(e)+")")
        else:
            try:
                self.tweets.replace_one({"id": self.data['id']},self.data)
            except Exception as e:
                print("ERROR UPDATING TWEET ("+str(e)+")")

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
                print("ERROR SEARCHING FOR USER")
        if (self.database=='messages'):
            try:
                result = self.messages.find_one({"id": self.data['id']})
                if(result):
                    return True
                else:
                    return False
            except:
                print("ERROR SEARCHING FOR MESSAGE")
        else:
            try:
                result = self.tweets.find_one({"id": self.data['id']})
                if(result):
                    return True
                else:
                    return False
            except Exception as e:
                print("ERROR SEARCHING FOR TWEET: "+str(e))
    
    def getUsers(self):
        return self.users.find({})

    def getTweets(self):
        return self.tweets.find({})