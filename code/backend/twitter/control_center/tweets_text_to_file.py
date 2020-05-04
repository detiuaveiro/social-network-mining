import json
import os
from typing import List

from control_center.utils import tweet_to_simple_text
from wrappers.mongo_wrapper import MongoAPI

FIELDS = ['text', 'full_text']
DIR_EXPORT = "tweets_text/"
MIN_SIZE_TWEET = 3


class TweetsExporter:
	def __init__(self):
		self.mongo_api = MongoAPI()

	def get_tweets(self) -> List[dict]:
		results = []
		for field in FIELDS:
			results += self.mongo_api.search(collection='tweets', query={field: {'$exists': True, '$ne': ''}},
			                                fields=[field])

		for result in results:
			if 'full_text' in result:
				result['text'] = result['full_text']
				del result['full_text']
			result['text'] = tweet_to_simple_text(result['text'])

		results = [result for result in results if len(result['text']) > MIN_SIZE_TWEET]

	def export_json(self, file_name: str):
		path = f"{DIR_EXPORT}{file_name}"
		if not os.path.exists(DIR_EXPORT):
			os.makedirs(DIR_EXPORT)

		results = self.get_tweets()

		with open(path, 'w') as file:
			file.write(json.dumps(results, ensure_ascii=False, indent=3))
