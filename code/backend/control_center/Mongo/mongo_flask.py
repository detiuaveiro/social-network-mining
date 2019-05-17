from flask import Flask
from flask_pymongo import PyMongo

class AppMongo:
	def __init__(self, appFlask, db):
		appFlask.config["MONGO_URI"] = "mongodb://192.168.85.46:32769/twitter."+db
		self.app = PyMongo(appFlask)
	
	def dataCollection(self, findText={}):
		return list(self.app.db.users.find(findText,projection={'_id':False}))

	def twitterCollection(self, findText={}):
		return list(self.app.db.tweets.find(findText,projection={'_id':False}))

	def getOneFilteredDoc(self, findText={},projection={'_id':False}):
		return list(self.app.db.users.find(findText,projection))


	def aggregate(self,pipeline):
		return list(self.app.db.users.aggregate(pipeline))
	
	def getCount(self, findText={}):
		return self.app.db.users.count_documents(findText)		
