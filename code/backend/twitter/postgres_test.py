from wrappers.postgresql_wrapper import PostgresAPI
from log_actions import RETWEET_REQ

psql = PostgresAPI()
psql.insert_log({
	"bot_id": 123412345,
	"action": RETWEET_REQ,
	"target_id": 87741
})

res = psql.search_logs({"target_id": 87741})

print(res)