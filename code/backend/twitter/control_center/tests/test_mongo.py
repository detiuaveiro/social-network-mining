from control_center.mongo_utils import BLANK_TWEET
from wrappers.mongo_wrapper import MongoAPI
from random import randint

mongo = MongoAPI()


def test_bulk_insert():
	for i in range(5):
		tweet = BLANK_TWEET.copy()
		tweet_id = randint(1000000, 1000001)
		tweet["id"] = tweet_id
		tweet["id_str"] = str(tweet_id)
		mongo.insert_tweets(tweet)
	mongo.save()


if __name__ == "__main__":
	test_bulk_insert()
