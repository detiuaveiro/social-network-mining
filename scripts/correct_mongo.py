from pymongo import MongoClient
import argparse

mongo = MongoClient("mongodb://localhost:27017")

users = eval(f"mongo.twitter.users")
tweets = eval(f"mongo.twitter.tweets")
messages = eval(f"mongo.twitter.messages")


def update_mongo(check_prints):
	list_of_tweets = tweets.find({"$or": [{"user": {"$type": "long"}}, {"user": {"$type": "number"}}]},
								 ["id_str", "user"])
	list_of_tweets = list(list_of_tweets)
	if check_prints:
		print(list_of_tweets)

	for tweet in list_of_tweets:
		user_doc = users.find_one({"id": tweet["user"]}, {"_id": 0})
		tweets.update_many({"id_str": tweet["id_str"]}, {"$set": {"user": user_doc}})

	list_of_tweets = tweets.find({"$or": [{"user": {"$type": "long"}}, {"user": {"$type": "number"}}]},
								 ["id_str", "user"])
	
	list_of_tweets = list(list_of_tweets)
	if check_prints:
		print(list_of_tweets)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('--verbose', help='Print more data',
						action='store_true')

	args = parser.parse_args()
	update_mongo(args.verbose)
