from pymongo import MongoClient

class MongoAPI():
    def __init__(self):
        print("Connecting to MongoDB")
        self.client = MongoClient('mongodb://192.168.85.46:32769/')
        self.users = self.client.twitter.users
        self.tweets = self.client.twitter.tweets

    def save(self, database, data):
        self.database = database
        self.data = data

        if (self.database=='users'):
            try:
                self.users.insert_one(self.data)
            except:
                print("WARNING: ERROR INSERTING USER")
        else:
            try:
                self.tweets.insert_one(self.data)
            except:
                print("WARNING: ERROR INSERTING TWEET")

    def update(self, database, data):
        self.database = database
        self.data = data

        if (self.database=='users'):
            try:
                self.users.replace_one({"id": self.data['data']['id']},self.data)
            except Exception as e:
                print("WARNING: ERROR UPDATING USER ("+str(e)+" )")
        else:
            try:
                self.tweets.replace_one({"id": self.data['data']['id']},self.data)
            except Exception as e:
                print("WARNING: ERROR UPDATING TWEET ("+str(e)+" )")
                
    def search(self, database, data):
        self.database = database
        self.data = data
        result
        if (self.database=='users'):
            try:
                result = self.users.find({"id": self.data['id']})
            except:
                print("WARNING: ERROR SEARCHING FOR USER")
        else:
            try:
                result = self.tweets.find({"id": self.data['id']})
            except:
                print("WARNING: ERROR SEARCHING FOR TWEET")
        if(len(result)==0):
            return False
        else:
            return True