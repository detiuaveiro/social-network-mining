import log_actions
from wrappers.postgresql_wrapper import PostgresAPI

if __name__ == "__main__":
	post = PostgresAPI()
	post.insert_log({
		"bot_id": 1234,
		"action": log_actions.TWEET_LIKE,
		"target_id": 1232123
	})

	post.insert_log({
		"bot_id": 1234,
		"action": "ERROR: FAILED TO DO SOMETHING IDK"
	})

	print(post.search_logs(params={"bot_id": 1234}))
	print(post.search_logs(params={"action": log_actions.TWEET_LIKE}))
	print(post.search_logs(params={"target_id": 1232123}))
	print(post.search_logs(params={"bot_id": 1234, "target_id": 1232123}))
