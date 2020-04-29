from control_center.tests.save_tweet_relations import test
from control_center.tests import test_logs


def main():
	#test_json()
	test.test_neo4j()
	test_logs.test_logs_ts()
	test_logs.test_logs()


if __name__ == "__main__":
	main()
