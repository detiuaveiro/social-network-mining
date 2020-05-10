from wrappers.postgresql_wrapper import PostgresAPI
import log_actions
from datetime import timedelta, datetime
import pytz

psql = PostgresAPI()


def test_logs_ts():
	utc = pytz.UTC
	result = psql.search_logs(
		params={"bot_id": 1234, "action": "TWEET_LIKE", "target_id": 1232123},
		limit=1
	)
	if result["success"] and len(result['data']) > 0:
		log = (timedelta(hours=1) + result['data'][0]['timestamp']).replace(tzinfo=utc)  # utc.localize()
		now = datetime.now().replace(tzinfo=utc)  # utc.localize()
		print(now > log)
	timestamp = timedelta(days=10) + datetime.now()ee
	result = psql.search_logs(
		params={"bot_id": 1234, "action": "TWEET_LIKE", "target_id": 1232123, "timestamp": timestamp},
		limit=10
	)
	print(result)


def test_logs():
	results = psql.search_logs({
		"action": log_actions.FOLLOW,
		"target_id": 31868
	})

	if results['success'] and len(results['data']) > 0:
		print("Found follow")