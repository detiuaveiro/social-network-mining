from wrappers.mongo_wrapper import MongoAPI
from control_center import mongo_utils as utils
import argparse
import random
import string

mongo = MongoAPI()


def update_mongo(check_prints):

	list_of_tweets = mongo.search("tweets", {"$or": [{"user": {"$type": "long"}}, {"user": {"$type": "number"}}]}, ["id_str", "user"])
	if check_prints:
		print(list_of_tweets)

	for tweet in list_of_tweets:
		user_doc = mongo.users.find_one({"id": tweet["user"]})
		if user_doc:
			mongo.update_tweets({"id_str": tweet["id_str"]}, {"user": user_doc})
		else:
			if check_prints:
				print("Found user none")
			blank_user = utils.BLANK_USER.copy()
			blank_user["id"] = tweet["user"]
			blank_user["id_str"] = str(tweet["user"])

			letters = string.ascii_lowercase
			blank_user["screen_name"] = ''.join(random.choice(letters) for i in range(8))
			mongo.insert_users(blank_user)
			mongo.update_tweets({"id_str": tweet["id_str"]}, {"user": blank_user})

	list_of_tweets = mongo.search("tweets", {"user": {"$type": "long"}}, ["id_str", "user"])
	if check_prints:
		print(list_of_tweets)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('--verbose', help='Print more data',
						action='store_true')

	args = parser.parse_args()
	update_mongo(args.verbose)
