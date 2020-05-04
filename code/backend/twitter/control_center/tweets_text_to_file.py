from __future__ import annotations
import json
import os
from enum import Enum
from typing import List

from control_center.utils import tweet_to_simple_text
from wrappers.mongo_wrapper import MongoAPI

FIELDS = ['text', 'full_text']
DIR_EXPORT = "tweets_text/"
MIN_SIZE_TWEET = 3


class TweetsExporter:
	def __init__(self):
		self.mongo_api = MongoAPI()

	def __get_tweets(self) -> List[dict]:
		results = []
		for field in FIELDS:
			results += self.mongo_api.search(collection='tweets', query={field: {'$exists': True, '$ne': ''}},
			                                fields=[field])

		for result in results:
			if 'full_text' in result:
				result['text'] = result['full_text']
				del result['full_text']
			result['text'] = tweet_to_simple_text(result['text'])

		return [result for result in results if len(result['text']) > MIN_SIZE_TWEET]

	def export(self, file_name: str, output_type: TweetsExporter.OutputType):
		if output_type == self.OutputType.TEXT:
			self.__export_text(f"{file_name}.{output_type.value}")
		elif output_type == self.OutputType.JSON:
			self.__export_json(f"{file_name}.{output_type.value}")

	def __export_json(self, file_name: str):
		path = f"{DIR_EXPORT}{file_name}"
		self.__create_dir()

		results = self.__get_tweets()

		with open(path, 'w') as file:
			file.write(json.dumps(results, ensure_ascii=False, indent=3))

	def __export_text(self, file_name: str):
		self.__create_dir()
		path = f"{DIR_EXPORT}{file_name}"

		results = self.__get_tweets()

		with open(path, 'w') as file:
			for result in results:
				file.write(f"{result['text']}\n")

	@staticmethod
	def __create_dir():
		if not os.path.exists(DIR_EXPORT):
			os.makedirs(DIR_EXPORT)


	class OutputType(Enum):
		TEXT = "txt"
		JSON = "json"

		def __str__(self):
			return self.name
