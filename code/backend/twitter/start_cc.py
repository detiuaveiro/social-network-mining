## @package twitter
import argparse

from control_center.control_center import Control_Center
from control_center.text_generator import test_smarter_replier
from control_center.tweets_text_to_file import TweetsExporter


def main():
	control_center = Control_Center()
	control_center.run()
	control_center.close()


def tests(test_type):
	if test_type == "text_generator":
		test_smarter_replier()


def export_tweets_text(file_name: str):
	exporter = TweetsExporter()
	exporter.export(file_name)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--test', type=str, default='')
	parser.add_argument('--export_tweets_text', type=str, default='tweets.json')
	args = parser.parse_args()

	if args.test:
		tests(args.test)
	if args.export_tweets_text:
		export_tweets_text(args.export_tweets_text)
	else:
		main()
