## @package twitter
import argparse

from control_center.text_generator import test_smarter_replier
from control_center.tweets_text_to_file import TweetsExporter
from wrappers.rabbitmq_wrapper import Rabbitmq


def main():
	control_center = Rabbitmq()
	while True:
		print("ola")
		control_center.run()
	# control_center.close()


def tests(test_type):
	if test_type == "text_generator":
		test_smarter_replier()


def export_tweets_text(file_name: str):
	exporter = TweetsExporter()
	exporter.export(file_name, TweetsExporter.OutputType.TEXT)


def export_tweets_json(file_name: str):
	exporter = TweetsExporter()
	exporter.export(file_name, TweetsExporter.OutputType.JSON)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--test', type=str)
	parser.add_argument('--export_tweets_text', type=str)
	parser.add_argument('--export_tweets_json', type=str)
	args = parser.parse_args()

	if args.test:
		tests(args.test)
	elif args.export_tweets_text:
		export_tweets_text(args.export_tweets_text)
	elif args.export_tweets_json:
		export_tweets_json(args.export_tweets_json)
	else:
		main()
