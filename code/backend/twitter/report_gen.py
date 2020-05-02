import os
import csv
import json
import logging
from enum import IntEnum

from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI


logger = logging.getLogger("report")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("report_gen.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


EXPORT_DIR = "export"


class Report:
	class ExportType(IntEnum):
		"""
		Enum for the Messages sent by the bot to the server.
		"""

		CSV = 0
		JSON = 1

		def __str__(self):
			return self.name

	def __init__(self):
		self.mongo = MongoAPI()
		self.neo = Neo4jAPI()
		self.exporter = Report.__Exporter(EXPORT_DIR)

	def __node_builder(self, node):
		node_start = "("

		if len(node) > 0:
			if "label" in node:
				node_start += ":" + "|".join(node['label'])
			elif

		return node_start+")"

	def create_report(self, match: dict, params: dict, limit: int = None, export='csv'):
		query = "MATCH "
		if not params:
			params = {}

		query = match + " RETURN " + ",".join(params.keys())

		if limit:
			query += " limit " + str(limit)

		result = []
		logger.info(self.neo.export_query(query, rel_node_properties=True))
		for row in self.neo.export_query(query, rel_node_properties=True):
			row_dict = {}
			for key in row:
				if type(row[key]) is dict:
					if row[key]['labels'] == ['Tweet']:
						row_dict[key] = self.mongo.search(
							'tweets', query={"id_str": row[key]['properties']['id']}, fields=params[key], single=True)
						if not row_dict[key]:
							row_dict[key] = {prop: None for prop in params[key]}
					else:
						row_dict[key] = self.mongo.search(
							'users', query={"id_str": row[key]['properties']['id']}, fields=params[key], single=True)
						if not row_dict[key]:
							row_dict[key] = {prop: None for prop in params[key]}
				else:
					row_dict[key] = {'name': row[key][0]['label']}
			result.append(row_dict)

		if export == self.ExportType.CSV:
			self.exporter.export_csv(result)
		elif export == self.ExportType.JSON:
			self.exporter.export_json(result)

	class __Exporter:
		def __init__(self, directory):
			self.directory = directory

			if not os.path.exists(self.directory):
				os.makedirs(self.directory)

		def export_csv(self, result):
			headers = [key + "_" + prop for key in result[0] for prop in result[0][key]]
			try:
				with open(f"{self.directory}/export.csv", 'w') as file:
					writer = csv.writer(file)
					writer.writerow(headers)
					for data in result:
						writer.writerow([data[key][prop] for key in data for prop in data[key]])
			except Exception as error:
				logger.exception(f"Occurred an error <{error}>: ")

		def export_json(self, result):
			try:
				with open(f"{self.directory}/export.json", "w") as file:
					json.dump(result, file)
			except Exception as error:
				logger.exception(f"Occurred an error <{error}>: ")


if __name__ == '__main__':
	rep = Report()
	query = {
		'start': {},
		'rel': {
			'depth_start': 2,
			'depth_end': 4,
			'label': ['FOLLOWS', 'WROTE']
		},
		'end': {
			'label': 'User'
		}
	}
	params = {
		'start': {
			'Tweet': ['retweet_count', 'favourite_count', 'text'],
			'User': ['name', 'screen_name', 'followers_count', 'friends_count', 'verified'],
			'Bot': ['name', 'screen_name', 'followers_count', 'friends_count']
		},
		'inter': {
			'Tweet': [],
			'User': ['name', 'screen_name'],
			'Bot': ['name']
		},
		'end': {
			'Tweet': ['favorite_count'],
			'User': ['listed_count'],
			'Bot': ['friends_count']
		}
	}
	limit = 1
	for export_type in Report.ExportType:
		print(export_type)
		rep.create_report(query, params, limit, export_type)
#
#
#
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
