from pymongo import MongoClient

class MongoAPI():
    def __init__(self):
        self.client = MongoClient('mongodb://192.168.85.46:32769/')
        self.users = self.client.twitter.users
        self.tweets = self.client.twitter.tweets

    def save(self, database, data):
        self.database = database
        self.data = data

        if (self.database=='users'):
            self.users.insert_one(self.data)
        else:
            self.tweets.insert_one(self.data)

