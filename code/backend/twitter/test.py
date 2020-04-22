from wrappers.neo4j_wrapper import Neo4jAPI
from wrappers.mongo_wrapper import MongoAPI

if __name__ == "__main__":
	mongo = MongoAPI()
	neo = Neo4jAPI()

	print(mongo.search(
		collection="tweets",
		query={"is_quote_status": True},
		fields=["in_reply_to_status_id"]
	))

	neo.add_user({"id": 0, "name": "DS", "username": "FenixD.S"})
	neo.add_tweet({"id": 1})
	neo.add_writer_relationship({"tweet_id": 1, "user_id": 0, "user_type": "User"})

	neo.add_user({"id": 2, "name": "Jonas", "username": "Jonas_Pistolas"})
	neo.add_tweet({"id": 3})
	neo.add_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"})

	neo.add_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"})
	neo.add_reply_relationship({"tweet": 1, "reply": 3})

	print(neo.check_tweet_exists(1))
	print(neo.check_tweet_exists(3))
	print(neo.check_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"}))
	print(neo.check_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"}))
	print(neo.check_reply_relationship({"tweet": 1, "reply": 3}))

	neo.delete_user(0)
	neo.delete_tweet(1)
	neo.delete_writer_relationship({"tweet_id": 1, "user_id": 0, "user_type": "User"})

	neo.delete_user(2)
	neo.delete_tweet(3)
	neo.delete_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"})

	neo.delete_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"})
	neo.delete_reply_relationship({"tweet": 1, "reply": 3})

