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
		query_node = "("

		if len(node) > 0:
			if "label" in node:
				query_node += ":" + "|".join(node['label'])

		return query_node+")"

	def __relation_builder(self, rel):
		query_rel = "["
		if len(rel) > 0:
			if 'label' in rel:
				query_rel += ":" + "|".join(rel['label'])
			if 'depth_start' in rel:
				query_rel += "*" + str(rel['depth_start'])
			if 'depth_end' in rel:
				query_rel += ".."+str(rel['depth_end'])
		return query_rel + "]"

	def __get_mongo_info(self, node, params):
		node_type = node["labels"][0]

		if node_type in params and len(params[node_type]) > 0:
			if node_type == "Tweet":
				mongo_info = self.mongo.search('tweets', query={"id_str": node['properties']['id']},
										 fields=params[node_type], single=True)
			# It's a user or a bot
			else:
				mongo_info = self.mongo.search('users', query={"id_str": node['properties']['id']},
											 fields=params[node_type], single=True)
			if mongo_info:
				return mongo_info
			return {param: None for param in params[node_type]}
		return None

	def __get_mongo_aggregate(self, table, query, params):
		params += ["id_str"]
		if len(query) != 0:
			result = self.mongo.search(table, query={"$or": query}, fields=params)

			if not result:
				result = {param: None for param in params}

			return result
		return None

	def create_report(self, match: dict, params: dict, limit: int = None, export='csv'):
		query = f"MATCH r={self.__node_builder(match['start'])}" \
				f"-{self.__relation_builder(match['rel'])}" \
				f"->{self.__node_builder(match['end'])} " \
				f"return r"
		logger.info(query)

		if limit:
			query += " limit " + str(limit)

		result = []

		query_result = self.neo.export_query(query, rel_node_properties=True)

		logger.debug(query_result)

		for row in query_result:
			# Analyse each row by looking at its rels field
			relations = row['r']['rels']
			relation = {}

			# Add the detailed start node
			node_mongo_info = self.__get_mongo_info(relations[0]["start"], params['start'])
			if node_mongo_info:
				relation['start'] = node_mongo_info

			for index in range(len(relations) - 1):
				rel = relations[index]
				relation['rel' + str(index+1)] = {"name": rel["label"]}
				node_mongo_info = self.__get_mongo_info(rel["end"], params['inter'])
				if node_mongo_info:
					relation['inter' + str(index)] = node_mongo_info

			# Add ending node
			relation['rel' + str(len(relations))] = {"name": relations[-1]["label"]}
			node_mongo_info = self.__get_mongo_info(relations[-1]["end"], params['end'])
			logger.debug(node_mongo_info)
			if node_mongo_info:
				relation['end'] = node_mongo_info

			# Append to result
			result.append(relation)

		#logger.debug(result)

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
			'depth_start': 5,
		},
		'end': {}
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
	limit = 10000
	for export_type in Report.ExportType:
		print(export_type)
		rep.create_report(query, params, limit, export_type)
#
#
#
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
