from flask import Flask
from flask_pymongo import PyMongo
import json
import csv

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

	def exportTweets(self,fields=None,export_type="json"):
		if export_type == "json":			
			with open("data.json","w") as f:
				if fields is None:
					data=list(self.app.db.tweets.find({},projection={'_id':False}))
				else:
					fields.update({'_id':False})
					data=list(self.app.db.tweets.find({},projection=fields))
				json.dump(data,f)
			fil=open("data.json","r+")

		elif export_type == "csv":
			entities_updated={}
			with open("data.csv","w") as f:
				if fields is None:
					data=list(self.app.db.tweets.find({},projection={'_id':False,"possibly_sensitive":False}))
					fields=list(data[0].keys())
					fields.append("quoted_status_id");fields.append("hashtags");fields.append("urls");fields.append("user_mentions");fields.append("symbols");fields.append("media");fields.append("polls");fields.remove("entities")
					writer=csv.DictWriter(f,fields)
					writer.writeheader()
					for document in data:
						entities=document["entities"]
						del document["entities"]
						for i in entities:
							try:
								entities_updated[i]=entities[i]
							except KeyError:
								pass
						document.update(entities_updated)
						writer.writerow(document)
					
				else:
					fields.update({'_id':False})
					data=list(self.app.db.tweets.find({},projection=fields))
					field=list(fields.keys())
					field.remove('_id')
					if "entities" in field:
						field.append("hashtags");field.append("urls");field.append("user_mentions");field.append("symbols");field.append("media");field.append("polls");field.remove("entities")
					writer=csv.DictWriter(f,field)
					writer.writeheader()
					for document in data:
						entities=document["entities"]
						del document["entities"]
						for i in entities:
							try:
								entities_updated[i]=entities[i]
							except KeyError:
								pass
						document.update(entities_updated)
						writer.writerow(document)
			fil=open("data.csv","r+")

		else:
			return {"NotImplementedError":"Not implemented yet!"}
		return fil