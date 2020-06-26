## @package twitter.wrappers
# coding: UTF-8

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import logging
import json
import credentials as credentials

log = logging.getLogger("Mongo")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("mongo.log", "w"))
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

        self.users = eval(f"self.client.{credentials.MONGO_DB}.users")
        self.tweets = eval(f"self.client.{credentials.MONGO_DB}.tweets")
        self.messages = eval(f"self.client.{credentials.MONGO_DB}.messages")

        self.list_of_users = []
        self.list_of_tweets = []
        self.list_of_messages = []

        self.index_of_users = {}
        self.index_of_tweets = {}
        self.index_of_messages = {}

    # TODO - IMPLEMENT ME PLEASE!
    def verify_integrity(self, collection, document):
        """Verifies if the document to be inserted has the same structure as the other documents in the collection

        @param collection: The collection we want to insert the document into
        @param document: The document we want to insert
        @return: True or false whether the integrity is verified or not
        """
        pass

    def get_count(self, collection, data={}):
        """Gets the total number of documents in a given collection

        @param collection: The collection we want to count the documents in
        @param data: The params we want the counted documents to have. By default it counts all documents
        @return: The number of documents in a given collection
        """
        if collection not in ["users", "tweets", "messages"]:
            log.error("ERROR GETTING DOCUMENT COUNT")
            log.error("Error: Unknown Collection. Please use users, tweets or messages")
        else:
            try:
                if collection == "users":
                    return self.users.count_documents(data)
                elif collection == "tweets":
                    return self.tweets.count_documents(data)
                else:
                    return self.messages.count_documents(data)
            except Exception as error:
                log.exception(f"ERROR <{error}> GETTING DOCUMENT COUNT for data <{data}>: ")

    def insert_users(self, data):
        """Inserts a new single document into our Users Collection

        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        if data["id_str"] not in self.index_of_users:
            self.index_of_users[data["id_str"]] = len(self.list_of_users)
            self.list_of_users.append(data)
            log.debug("INSERT SUCCESSFUL")
        else:
            self.list_of_users[self.index_of_users[data["id_str"]]] = data
            log.debug("UPDATE SUCCESSFUL ON BULK INSERT")

    def insert_tweets(self, data):
        """Inserts a new single document into our Tweets Collection

        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        if data["id_str"] not in self.index_of_tweets:
            self.index_of_tweets[data["id_str"]] = len(self.list_of_tweets)
            self.list_of_tweets.append(data)
            log.debug("INSERT SUCCESSFUL")
        else:
            self.list_of_tweets[self.index_of_tweets[data["id_str"]]] = data
            log.debug("UPDATE SUCCESSFUL ON BULK INSERT")

    def insert_messages(self, data):
        """Inserts a new single document into our Messages Collection

        @param data: The document to be inserted. Should be in the form of a dictionary
        """
        if data["id_str"] not in self.index_of_messages:
            self.index_of_messages["id_str"] = len(self.list_of_messages)
            self.list_of_messages.append(data)
            log.debug("INSERT SUCCESSFUL")
        else:
            self.list_of_messages[self.index_of_messages["id_str"]] = data
            log.debug("UPDATE SUCCESSFUL ON BULK INSERT")

    def update_users(self, match, new_data, all=True):
        """Updates one or many documents on Users Collection

        @param match: The params the documents we want to update must fulfill
        @param new_data: The new data we want to place
        @param all: Whether we want to update all or just the first document found
        """
        try:
            if all:
                self.users.update_many(match, {"$set": new_data})
            else:
                self.users.update_one(match, {"$set": new_data})
            log.debug("UPDATE SUCCESSFUL")
        except Exception as error:
            log.exception(f"ERROR <{error}> UPDATING DOCUMENT with match <{match}> and data <{new_data}>: ")

    def update_tweets(self, match, new_data, all=True):
        """Updates one or many documents on Tweets Collection

        @param match: The params the documents we want to update must fulfill
        @param new_data: The new data we want to place
        @param all: Whether we want to update all or just the first document found
        """
        try:
            if all:
                self.tweets.update_many(match, {"$set": new_data})
            else:
                self.tweets.update_one(match, {"$set": new_data})
            log.debug("UPDATE SUCCESSFUL")
        except Exception as error:
            log.exception(f"ERROR <{error}> UPDATING DOCUMENT with match <{match}> <{new_data}>: ")

    def update_messages(self, match, new_data, all=True):
        """Updates one or many documents on Messages Collection

        @param match: The params the documents we want to update must fulfill
        @param new_data: The new data we want to place
        @param all: Whether we want to update all or just the first document found
        """
        try:
            if all:
                self.messages.update_many(match, {"$set": new_data})
            else:
                self.messages.update_one(match, {"$set": new_data})
            log.debug("UPDATE SUCCESSFUL")
        except Exception as error:
            log.exception(f"ERROR <{error}> UPDATING DOCUMENT with match <{match}> and data <{new_data}>: ")

    def search(
            self,
            collection: str,
            query: dict = None,
            fields: list = None,
            single: bool = False,
            export_type: str = None,
    ):
        """Searches the a collection by a given search query. Can also export to a json or csv

        @param collection: Specifies the collection we want to query
        @param query: The search query we're using. By default it finds all documents
        @param fields: Specifies the fields we want to show on the query result
        @param single: Whether we want to search only for one document or for all that match the query. By default
        we search for all
        @param export_type: Specifies whether or not to export the result. Can either be None, json or csv
        @return: The search result
        """
        if not query:
            query = {}

        if collection not in ["users", "tweets", "messages"]:
            log.error("ERROR SEARCHING FOR DOCUMENTS")
            log.debug("Error: ", "Unknown Collection. Please use users, tweets or messages")
            return

        try:
            if fields:
                projection = {"_id": False}
                for i in fields:
                    projection[i] = True
            else:
                projection = {"_id": True}

            # log.debug(query)
            # log.debug(projection)

            result = None
            if single:
                if collection == "tweets":
                    result = self.tweets.find_one(query, projection)
                if collection == "messages":
                    result = self.messages.find_one(query, projection)
                if collection == "users":
                    result = self.users.find_one(query, projection)
            else:
                if collection == "tweets":
                    result = self.tweets.find(query, projection)
                if collection == "messages":
                    result = self.messages.find(query, projection)
                if collection == "users":
                    result = self.users.find(query, projection)

            # Optionally export result
            if export_type is not None:
                return self.__export_data(result, export_type)

            if result is None:
                return None
            else:
                if single:
                    return dict(result)
                else:
                    return list(result)
        except Exception as error:
            log.exception(f"ERROR <{error}> SEARCHING FOR DOCUMENT with query <{query}>: ")

    def save_tweets(self):
        if len(self.list_of_tweets) != 0:
            try:
                self.tweets.insert_many(self.list_of_tweets, ordered=False)
            except BulkWriteError as bwe:
                log.exception(f"BULK ERRORS OCCURRED: <{bwe.details}>")
            except Exception as error:
                log.exception(f"ERROR <{error}> INSERTING TWEETS, INSERTING ONE BY ONE")
            self.list_of_tweets = []
            self.index_of_tweets = {}

        log.info("Saved all tweets")

    def save_users(self):
        if len(self.list_of_users) != 0:
            try:
                self.users.insert_many(self.list_of_users, ordered=False)
            except BulkWriteError as bwe:
                log.exception(f"BULK ERRORS OCCURRED: <{bwe.details}>")
            except Exception as error:
                log.exception(f"ERROR <{error}> INSERTING USERS, INSERTING ONE BY ONE")
            self.list_of_users = []
            self.index_of_users = {}

        log.info("Saved all users")

    def save_messages(self):
        if len(self.list_of_messages) != 0:
            try:
                self.messages.insert_many(self.list_of_messages)
                self.list_of_messages = []
                self.index_of_messages = {}
            except Exception as error:
                log.exception(f"ERROR <{error}> INSERTING MESSAGES")

        log.info("Saved all messages")

    def save(self):
        """Bulk inserts the saved documents from previous inserts to the appropriate collections"""

        self.save_users()
        self.save_tweets()
        self.save_messages()

    def __export_data(self, data, export_type):
        """Exports a given array of documents into a csv or json

        @param data: An array of documents to export
        @param export_type: The type of the file we want to export to
        """
        if export_type == "json":
            return json.dumps(data, default=str)

        elif export_type == "csv":
            csv_content = ""

            # Get the header
            if len(data) != 0:
                field_names = list(data[0].keys())
                for field in field_names:
                    csv_content += field + ","
                csv_content = csv_content[:-1] + "\n"
            else:
                field_names = []

            # Get the values
            for row in data:
                for field in row:
                    csv_content += row[field] + ","
                csv_content = csv_content[:-1] + "\n"

            return csv_content[:-1]

        else:
            log.error("ERROR EXPORTING RESULT")
            log.error("Error: Specified export type not supported. Please use json or csv")


if __name__ == "__main__":
    mongo = MongoAPI()
    #
    #    #Inserting a document
    #    mongo.insert_tweets({"name": "ds"})
    #    mongo.insert_users({"name": "ds"})
    #    mongo.insert_messages({"name": "ds"})
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
    #    print(mongo.get_count("users"))
    #    print(mongo.get_count("tweets"))
    #    print(mongo.get_count("messages", {"name": "ds"}))

    # print(mongo.search(collection="messages",fields=["name"]))

    # mongo.search(collection="messages",fields=["name"], export_type="json")
    # mongo.search(collection="tweets",export_type="json")
    # mongo.search(collection="users",query={"name": "ds"}, export_type="json")

    # mongo.search(collection="messages", fields=["name"], export_type="csv")
    # mongo.search(collection="tweets", export_type="csv")
    # mongo.search(collection="users", query={"name": "ds"}, export_type="csv")
