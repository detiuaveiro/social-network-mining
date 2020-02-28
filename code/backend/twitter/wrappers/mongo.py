from pymongo import MongoClient
import logging
import sys

sys.path.append("..")
import credentials

log = logging.getLogger("Mongo")
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)

### Mongo Wrapper


class MongoAPI:
    """Mongo Wrapper

    Class responsible for all CRUD methods related to our mongo database
    """

    def __init__(self):
        log.debug("Connecting to MongoDB")
        self.client = MongoClient("mongodb://" + credentials.MONGO_FULL_URL)

        self.users = self.client.snm_mongo.users
        self.tweets = self.client.snm_mongo.tweets
        self.messages = self.client.snm_mongo.messages

    def insert_users(self, data):
        """Insert Users

        Inserts a new single document into our Users Collection
        @param data The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.users.insert_one(data)
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_users(self, query, single=False):
        """Search Users

        Searches the Users collection by a given search query
        @param query The search query we're using
        @param single Whether we want to search only for one document or for all that match the query. By default we search for all
        """
        try:
            if single:
                self.users.find_one(query)
            else:
                self.users.find(query)
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)

    def insert_tweets(self, data):
        """Insert Users

        Inserts a new single document into our Tweets Collection
        @param data The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.tweets.insert_one(data)
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_tweets(self, query, single=False):
        """Search Tweets

        Searches the Tweets collection by a given search query
        @param query The search query we're using
        @param single Whether we want to search only for one document or for all that match the query. By default we search for all
        """
        try:
            if single:
                self.tweets.find_one(query)
            else:
                self.tweets.find(query)
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)

    def insert_messages(self, data):
        """Insert Users

        Inserts a new single document into our Messages Collection
        @param data The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.messages.insert_one(data)
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_messages(self, query, single=False):
        """Search Messages

        Searches the Messages collection by a given search query
        @param query The search query we're using
        @param single Whether we want to search only for one document or for all that match the query. By default we search for all
        """
        try:
            if single:
                self.tweets.find_one(query)
            else:
                self.tweets.find(query)
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)


if __name__ == "__main__":
    #TODO - Test functions
    mongo = MongoAPI()
    mongo.insert_tweets({"name": "ds"})
    print(mongo.client)
