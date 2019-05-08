from flask import Flask
from flask_pymongo import PyMongo

class AppMongo:
	def __init__(self, appFlask, db):
		appFlask.config["MONGO_URI"] = "mongodb://192.168.85.46:32769/"+db
		self.app = PyMongo(appFlask)
	
	def dataCollection(self, findText={}):
		return list(self.app.db.collection.find(findText,projection={'_id':False}))

	def getOneFilteredDoc(self, findText={},projection={'_id':False}):
		return list(self.app.db.collection.find(findText,projection))

	def aggregate(self,pipeline):
		return list(self.app.db.collection.aggregate(pipeline))
	
	def getCount(self, findText={}):
		return self.app.db.collection.count_documents(findText)

	def insertOneData(self, dataJson):
		self.app.db.collection.insert(dataJson)

	def removeData(self,data):
		self.app.db.collection.delete_one({})
		
