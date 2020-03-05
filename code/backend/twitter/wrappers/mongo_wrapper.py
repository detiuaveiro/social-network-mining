from pymongo import MongoClient
import logging
import sys
import json
import csv
import datetime
from twitter import credentials


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

	# TODO - IMPLEMENT ME PLEASE!
	def verify_integrity(self, collection, document):
		"""Verifies if the document to be inserted has the same structure as the other documents in the collection
        
        @param collection: The collection we want to insert the document into
        @param document: The document we want to insert
        @return: True or false wether the integrity is verified or not
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
			log.error(
				"Error: Unknown Collection. Please use users, tweets or messages"
			)
		else:
			try:
				if collection == "users":
					return self.users.count_documents(data)
				elif collection == "tweets":
					return self.tweets.count_documents(data)
				else:
					return self.messages.count_documents(data)
			except Exception as e:
				log.error("ERROR GETTING DOCUMENT COUNT")
				log.error("Error: ", e)

	def insert_users(self, data):
		"""Inserts a new single document into our Users Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
		try:
			self.users.insert_one(data)
			log.debug("INSERT SUCCESFUL")
		except Exception as e:
			log.error("ERROR INSERTING DOCUMENT")
			log.error("Error: ", e)

	def insert_tweets(self, data):
		"""Inserts a new single document into our Tweets Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
		try:
			self.tweets.insert_one(data)
			log.debug("INSERT SUCCESFUL")
		except Exception as e:
			log.error("ERROR INSERTING DOCUMENT")
			log.error("Error: ", e)

	def insert_messages(self, data):
		"""Inserts a new single document into our Messages Collection
        
        @param data: The document to be inserted. Should be in the form of a dictionary
        """
		try:
			self.messages.insert_one(data)
			log.debug("INSERT SUCCESFUL")
		except Exception as e:
			log.error("ERROR INSERTING DOCUMENT")
			log.error("Error: ", e)

	def search(
			self,
			collection,
			query={},
			fields=None,
			single=False,
			export_type=None,
			export_name=None,
	):
		"""Searches the a collection by a given search query. Can also export to a json or csv
        
        @param collection: Specifies the collection we want to query
        @param query: The search query we're using. By default it finds all documents
        @param fields: Specifies the fields we want to show on the query result
        @param single: Whether we want to search only for one document or for all that match the query. By default
        	we search for all
        @param export_type: Specifies whether or not to export the result. Can either be None, json or csv
        @param export_name: Specifies the path where to export to.
        @return: The search result
        """
		if collection not in ["users", "tweets", "messages"]:
			log.error("ERROR SEARCHING FOR DOCUMENTS")
			log.debug(
				"Error: ", "Unknown Collection. Please use users, tweets or messages"
			)

			return

		try:
			if fields is not None:
				projection = {"_id": False}
				for i in fields:
					projection[i] = True
			else:
				projection = None

			if single:
				if collection == "tweets":
					result = list(self.tweets.find_one(query, projection))
				if collection == "messages":
					result = list(self.messages.find_one(query, projection))
				if collection == "users":
					result = list(self.users.find_one(query, projection))
			else:
				if collection == "tweets":
					result = list(self.tweets.find(query, projection))
				if collection == "messages":
					result = list(self.messages.find(query, projection))
				if collection == "users":
					result = list(self.users.find(query, projection))

			# Optionally export result
			if export_type is not None:
				if export_name is None:
					export_name = (
							"../export_results/"
							+ export_type
							+ "/mongo_"
							+ collection
							+ "_"
							+ str(datetime.datetime.now()).replace(" ", "_")
					)
					export_name = (
						export_name + ".json"
						if export_type == "json"
						else export_name + ".csv"
					)

				self.__export_data(result, export_name, export_type)

			return result
		except Exception as e:
			log.error("ERROR SEARCHING FOR DOCUMENT")
			log.error("Error: ", e)

	def __export_data(self, data, export_name, export_type):
		"""Exports a given array of documents into a csv or json
        
        @param data: An array of documents to export
        @param export_name: The file path we want to export to
        @param export_type: The type of the file we want to export to
        """
		if export_type == "json":
			with open(export_name, "w") as writer:
				json.dump(data, writer, default=str)

		elif export_type == "csv":
			# Get the values
			if len(data) != 0:
				field_names = list(data[0].keys())
			else:
				field_names = []

			with open(export_name, "w") as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=field_names)

				writer.writeheader()

				for row in data:
					writer.writerow(row)

		else:
			log.error("ERROR EXPORTING RESULT")
			log.error(
				"Error: Specified export type not supported. Please use json or csv"
			)


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

	mongo.search(collection="messages", fields=["name"], export_type="csv")
	mongo.search(collection="tweets", export_type="csv")
	mongo.search(collection="users", query={"name": "ds"}, export_type="csv")
