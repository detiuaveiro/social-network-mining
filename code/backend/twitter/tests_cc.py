from control_center.tests.save_tweet_relations import test
from control_center.tests import test_logs, test_psql, test_redis, test_mongo
from wrappers.postgresql_wrapper import PostgresAPI
from report.report_gen import Report

def main():
	#test_json()
	#test.test_neo4j()
	#test_logs.test_logs_ts()
	#test_logs.test_logs()
	#test_psql.test_insert_user_with_protected()
	#print(test_redis.test_redis_ttl())
	test_mongo.test_bulk_insert()

if __name__ == "__main__":
	main()
