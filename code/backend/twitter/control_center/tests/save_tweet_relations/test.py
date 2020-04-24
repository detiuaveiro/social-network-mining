from wrappers.neo4j_wrapper import Neo4jAPI

if __name__ == "__main__":
	neo = Neo4jAPI()

	neo.delete_user(0)
	neo.delete_tweet(1)
	neo.delete_writer_relationship({"tweet_id": 1, "user_id": 0, "user_type": "User"})

	neo.delete_user(2)
	neo.delete_tweet(3)
	neo.delete_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"})

	neo.delete_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"})
	neo.delete_reply_relationship({"tweet": 1, "reply": 3})
	neo.delete_tweet(5)
	neo.delete_tweet(4)

	neo.add_user({"id": 0, "name": "DS", "username": "FenixD.S"})
	neo.add_tweet({"id": 1})
	neo.add_writer_relationship({"tweet_id": 1, "user_id": 0, "user_type": "User"})

	neo.add_user({"id": 2, "name": "Jonas", "username": "Jonas_Pistolas"})
	neo.add_tweet({"id": 3})
	neo.add_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"})

	neo.add_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"})
	neo.add_reply_relationship({"tweet": 1, "reply": 3})

	neo.add_bot({"id": 4, "name": "Fag", "username": "got"})
	neo.add_tweet({"id": 5})
	neo.add_writer_relationship({"tweet_id": 5, "user_id": 4, "user_type": "Bot"})
	neo.add_quote_relationship({"tweet_id": 5, "quoted_tweet": 1})

	print(neo.check_tweet_exists(1))
	print(neo.check_tweet_exists(3))
	print(neo.check_writer_relationship({"tweet_id": 3, "user_id": 2, "user_type": "User"}))
	print(neo.check_retweet_relationship({"tweet_id": 1, "user_id": 2, "user_type": "User"}))
	print(neo.check_reply_relationship({"tweet": 1, "reply": 3}))
	print(neo.check_quote_relationship({"tweet_id": 5, "quoted_tweet": 1}))


