from flask import Flask
from flask_pymongo import PyMongo
import json
import csv
import settings

class AppMongo:
	def __init__(self, appFlask, db):
		appFlask.config["MONGO_URI"] = "mongodb://"+settings.MONGO_FULL_URL+"/twitter."+db
		self.app = PyMongo(appFlask)
	
	def dataCollection(self, findText={}):
		return list(self.app.db.users.find(findText,projection={'_id':False}))

	def twitterCollection(self, findText={}):
		return list(self.app.db.tweets.find(findText,projection={'_id':False}))

	def getOneFilteredDoc(self, findText={},projection={'_id':False}):
		return list(self.app.db.users.find(findText,projection))

	def getMessagesForUser(self, findText={}):
		return list(self.app.db.messages.find(findText,projection={'_id':False}))

	def aggregate(self,pipeline):
		return list(self.app.db.users.aggregate(pipeline))
	
	def getCount(self, findText={}):
		return self.app.db.users.count_documents(findText)		

	def exportData(self,collection,fields=None,export_type="json"):
		if export_type == "json":
			with open("data.json","w") as f:
				keys={}
				if fields is None:
					if collection=="tweets":
						data=list(self.app.db.tweets.find({},projection={'_id':False}))
					else:
						data=list(self.app.db.users.find({},projection={'_id':False}))
				else:
					for i in fields:
						keys[i]=True
					keys.update({'_id':False})
					if collection=="tweets":
						data=list(self.app.db.tweets.find({},projection=keys))
					else:
						data=list(self.app.db.users.find({},projection=keys))
				json.dump(data,f)

		elif export_type == "csv":
			entities_updated={}
			with open("data.csv","w") as f:
				keys={}
				if fields is None:
					if collection=="tweets":
						data=list(self.app.db.tweets.find({},projection={'_id':False}))
					else:
						data=list(self.app.db.users.find({},projection={'_id':False}))
					fields=list(data[0].keys())
					if "entities" in fields:
						fields.append("id_str");fields.append("possibly_sensitive");fields.append("quoted_status_id");fields.append("hashtags");fields.append("urls");fields.append("user_mentions");fields.append("symbols");fields.append("media");fields.append("polls");fields.remove("entities")
					writer=csv.DictWriter(f,fields)
					writer.writeheader()
					if "hashtags" in fields:
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
						for document in data:
							writer.writerow(document)
					
				else:
					for i in fields:
						keys[i]=True
					keys.update({'_id':False})
					if collection=="tweets":
						data=list(self.app.db.tweets.find({},projection=keys))
					else:
						data=list(self.app.db.users.find({},projection=keys))
					field=list(keys.keys())
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
					else:
						writer=csv.DictWriter(f,field)
						writer.writeheader()
						for document in data:
							writer.writerow(document)

		else:
			return {"NotImplementedError":"Not implemented yet!"}
		return "OK"