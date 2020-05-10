from wrappers.postgresql_wrapper import PostgresAPI
from wrappers.mongo_wrapper import MongoAPI

psql = PostgresAPI()


def test_insert_user_with_protected():
	mongo = MongoAPI()
	user = mongo.search(collection="users", single=True,
						fields=["id", "followers_count", "friends_count", "protected"])
	user_psql = {
		"user_id": user['id'],
		"followers": user["followers_count"],
		"following": user["friends_count"],
		"protected": user["protected"]
	}
	psql.insert_user(user_psql)
	result = psql.search_user({"user_id": user['id']})
	print(result)
