from pymongo import MongoClient
import logging
import sys

sys.path.append("..")
import credentials

log = logging.getLogger("Mongo")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class MongoAPI:
    """Mongo Wrapper.

    Class that acts as a wrapper for all methods related to our Mongo DB 
    """

    def __init__(self):
        log.debug("Connecting to MongoDB")
        self.client = MongoClient("mongodb://" + credentials.MONGO_FULL_URL)

        self.users = self.client.snm_mongo.users
        self.tweets = self.client.snm_mongo.tweets
        self.messages = self.client.snm_mongo.messages

    #TODO - IMPLEMENT ME PLEASE!
    def verify_integrity(self, collection, document):
        """Verifies if the document to be inserted has the same structure as the other documents in the collection
        
        @param collection: The collection we want to insert the document into
        @param document: The document we want to insert
        @return: True or false wether the integrity is verified or not
        """
        pass

    def get_count(self, collection, data={}):
        """Gets the totl number of documents in a given collection
        
        @param collection: The collection we want to count the documents in
        @param data: The params we want the counted documents to have. By default it counts all documents
        @return: The number of documents in a given collection
        """
        if collection not in ["users", "tweets", "messages"]:
            log.info("ERROR GETTING DOCUMENT COUNT")
            log.debug("Error: ", "Unknown Collection. Please use users, tweets or messages")
        else:
            try:
                if collection == "users":
                    return self.users.count_documents(data)
                elif collection == "tweets":
                    return self.tweets.count_documents(data)
                else:
                    return self.messages.count_documents(data)
            except Exception as e:
                log.info("ERROR GETTING DOCUMENT COUNT")
                log.debug("Error: ", e)

    def insert_users(self, data):
        """Inserts a new single document into our Users Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.users.insert_one(data)
            log.debug("INSERT SUCCESFUL")
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_users(self, query={}, single=False):
        """Searches the Users collection by a given search query
        
        @param query: The search query we're using. By default it finds all documents
        @param single: Whether we want to search only for one document or for all that match the query. By default we search for all
        @return: The search result
        """
        try:
            if single:
                result = self.users.find_one(query)
            else:
                result = list(self.users.find(query))

            return result
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)

    def insert_tweets(self, data):
        """Inserts a new single document into our Tweets Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.tweets.insert_one(data)
            log.debug("INSERT SUCCESFUL")
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_tweets(self, query={}, single=False):
        """Searches the Tweets collection by a given search query
        
        @param query: The search query we're using. By default it finds all documents
        @param single: Whether we want to search only for one document or for all that match the query. By default we search for all
        @return: The search result
        """
        try:
            if single:
                result = self.tweets.find_one(query)
            else:
                result = list(self.tweets.find(query))

            return result
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)

    def insert_messages(self, data):
        """Inserts a new single document into our Messages Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        try:
            self.messages.insert_one(data)
            log.debug("INSERT SUCCESFUL")
        except Exception as e:
            log.info("ERROR INSERTING DOCUMENT")
            log.debug("Error: ", e)

    def search_messages(self, query={}, single=False):
        """Searches the Messages collection by a given search query
        
        @param query: The search query we're using. By default it finds all documents
        @param single: Whether we want to search only for one document or for all that match the query. By default we search for all
        @return: The search result
        """
        try:
            if single:
                result = self.tweets.find_one(query)
            else:
                result = list(self.tweets.find(query))

            return result
        except Exception as e:
            log.info("ERROR SEARCHING FOR DOCUMENT")
            log.debug("Error: ", e)



#if __name__ == "__main__":
#    mongo = MongoAPI()
#
#    #Inserting a document
#    mongo.insert_tweets({"name": "ds"})
#    mongo.insert_users({"name": "ds"})
#    mongo.insert_messages({"name": "ds"})
#
#    #Verifying the document was inserted
#    print(mongo.search_messages())
#    print(mongo.search_tweets())
#    print(mongo.search_users())
#
#    #Inserting a duplicate document
#    mongo.insert_tweets({"name": "ds"})
#    mongo.insert_users({"name": "ds"})
#    mongo.insert_messages({"name": "ds"})
#
#    #Inserting a new document
#    mongo.insert_tweets({"name": "escal"})
#    mongo.insert_users({"name": "escal"})
#    mongo.insert_messages({"name": "escal"})
#
#    #Verifying the documents were inserted
#    print(mongo.search_messages())
#    print(mongo.search_tweets())
#    print(mongo.search_users())
#
#    #Verifying the Search functions
#    print(mongo.search_messages({"name":"ds"}))
#    print(mongo.search_tweets({"name":"escal"}))
#    print(mongo.search_users({"name":"ds"}))
#
#    print(mongo.search_messages({"name":"ds"}, True))
#    print(mongo.search_tweets({"name":"escal"}, True))
#    print(mongo.search_users({"name":"ds"}, True))
#
#    print(mongo.get_count("users"))
#    print(mongo.get_count("tweets"))
#    print(mongo.get_count("messages", {"name": "ds"}))



