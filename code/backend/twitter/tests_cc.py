from control_center.tests.save_tweet_relations import test
from control_center.tests import test_psql
from wrappers.postgresql_wrapper import PostgresAPI
from datetime import timedelta, datetime
import pytz


def main():
	#test_json()
	#test.test_neo4j()
	test_psql.test_insert_user_with_protected()
	'''
	utc = pytz.UTC
	psql = PostgresAPI()
	result = psql.search_logs(
		params={"bot_id": 1234, "action": "TWEET_LIKE", "target_id": 1232123},
		limit=1
	)
	if result["success"]:
		log = (timedelta(hours=1) + result['data'][0]['timestamp']).replace(tzinfo=utc) #utc.localize()
		now = datetime.now().replace(tzinfo=utc) #  utc.localize()
		print(now > log)
	'''

if __name__ == "__main__":
	main()
