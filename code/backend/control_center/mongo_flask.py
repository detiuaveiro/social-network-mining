from flask import Flask
from flask_pymongo import PyMongo

class AppMongo:
	def __init__(self, appFlask, db):
		appFlask.config["MONGO_URI"] = "mongodb://192.168.85.46:32769/"+db
		self.app = PyMongo(appFlask)
	
	def dataCollection(self, findText={}):
		return list(self.app.db.collection.find(findText,projection={'_id':False}))

	def insertOneData(self, dataJson):
		self.app.db.collection.insert(dataJson)

	def removeData(self,data):
		self.app.db.collection.delete_one({})
		
