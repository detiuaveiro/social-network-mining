import os
import csv
import json
import logging
from enum import IntEnum

from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI


logger = logging.getLogger("bot-agents")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("bot_agent.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


EXPORT_DIR = "export"


class Report:
	def __init__(self):
		self.mongo = MongoAPI()
		self.neo = Neo4jAPI()
		self.exporter = Report.__Exporter(EXPORT_DIR)

	def create_report(self, match: str, params: dict = None, limit: int = None, export='csv'):
		if not params:
			params = {}

		query = match + " RETURN " + ",".join(params.keys())
		if limit:
			query += " limit " + str(limit)

		result = []
		logger.info(self.neo.export_query(query))
		for row in self.neo.export_query(query):
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

		if export == 'csv':
			self.exporter.export_csv(result)
		elif export == 'json':
			self.exporter.export_json(result)

	class ExportType(IntEnum):
		"""
		Enum for the Messages sent by the bot to the server.
		"""

		CSV = 0
		JSON = 1

		def __str__(self):
			return self.name

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


# if __name__ == '__main__':
# 	query = "MATCH (a: Tweet) - [r*3..4] - (b: User	)"
# 	params = {
# 		'a': ['text', 'favorite_count', 'retweet_count'],
# 		'b': ['name', 'screen_name', 'statuses_count'],
# 		'r': []
# 	}
# 	limit = 10
# 
# 	for export_type in Report.ExportType
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
# 