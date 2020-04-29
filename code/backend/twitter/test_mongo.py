from control_center.mongo_utils import BLANK_TWEET
from wrappers.mongo_wrapper import MongoAPI
from random import randint

mongo = MongoAPI()
for i in range(3):
	tweet = BLANK_TWEET.copy()
	id = randint(1000000, 2000000)
	tweet["id"] = id
	tweet["id_str"] = str(id)
	mongo.insert_tweets(tweet)