import os
import csv
import json
import logging
from enum import IntEnum
from time import time

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

	@staticmethod
	def __node_builder(node):
		query_node = "("

		if len(node) > 0:
			if "label" in node:
				query_node += ":" + "|".join(node['label'])

		return query_node+")"

	@staticmethod
	def __relation_builder(rel):
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
		if len(query) > 0 and len(params) > 0:
			result = self.mongo.search(table, query={"$or": [{"id_str": obj_id} for obj_id in query]}, fields=params)
			return result
		return None

	@staticmethod
	def __insert_info_list(info_dict, results_list, placement_dict):
		if results_list:
			for result in results_list:
				index, key = placement_dict[result["id_str"]]
				info_dict[index][key] = result
		return info_dict

	def __query_builder(self, query_tweets, query_bots, query_users, node):
		node_label = node["labels"][0]
		if node_label == "Tweet":
			query_tweets.append(node["properties"]["id"])
		elif node_label == "User":
			query_users.append(node["properties"]["id"])
		elif node_label == "Bot":
			query_bots.append(node["properties"]["id"])

	def create_report(self, match: dict, params: dict, limit: int = None, export='csv'):
		query = f"MATCH r={self.__node_builder(match['start'])}" \
				f"-{self.__relation_builder(match['rel'])}" \
				f"->{self.__node_builder(match['end'])} " \
				f"return r"
		logger.info(query)

		if limit:
			query += f" limit {limit}"

		result = []

		query_result = self.neo.export_query(query, rel_node_properties=True)

		#logger.debug(query_result)

		start = time()

		query_tweets_start = []
		query_tweets_interm = []
		query_tweets_end = []

		query_bots_start = []
		query_bots_interm = []
		query_bots_end = []

		query_user_start = []
		query_user_interm = []
		query_user_end = []

		keep_track_places = {}

		for row_index in range(len(query_result)):
			# Analyse each row by looking at its rels field
			row = query_result[row_index]
			relations = row['r']['rels']
			relation = {}

			# Add the detailed start node
			node_start = relations[0]["start"]
			self.__query_builder(query_tweets_start, query_bots_start, query_user_start, node_start)
			keep_track_places[node_start["properties"]["id"]] = (row_index, "start")
			relation["start"] = {param: None for param in params['start'][node_start["labels"][0]]}

			for index in range(len(relations) - 1):
				rel = relations[index]
				relation['rel' + str(index+1)] = {"name": rel["label"]}
				self.__query_builder(query_tweets_interm, query_bots_interm, query_user_interm, rel["end"])
				keep_track_places[rel["end"]["properties"]["id"]] = (row_index, "interm" + str(index + 1))
				relation["interm" + str(index+1)] = {param: None for param in params['inter'][rel["end"]["labels"][0]]}

			# Add ending node
			relation['rel' + str(len(relations))] = {"name": relations[-1]["label"]}
			node_end = relations[-1]["end"]
			self.__query_builder(query_tweets_end, query_bots_end, query_user_end, node_end)
			keep_track_places[node_end["properties"]["id"]] = (row_index, "end")
			relation["end"] = {param: None for param in params['end'][node_end["labels"][0]]}

			# Append to result
			result.append(relation)

		result_tweets_start = self.__get_mongo_aggregate("tweets", query_tweets_start, params['start']['Tweet'])
		result_users_start = self.__get_mongo_aggregate("users", query_user_start, params['start']['User'])
		result_bots_start = self.__get_mongo_aggregate("users", query_bots_start, params['start']['Bot'])

		result_tweets_interm = self.__get_mongo_aggregate("tweets", query_tweets_interm, params['inter']['Tweet'])
		result_users_interm = self.__get_mongo_aggregate("users", query_user_interm, params['inter']['User'])
		result_bots_interm = self.__get_mongo_aggregate("users", query_bots_interm, params['inter']['Bot'])

		result_tweets_end = self.__get_mongo_aggregate("tweets", query_tweets_end, params['end']['Tweet'])
		result_users_end = self.__get_mongo_aggregate("users", query_user_end, params['end']['User'])
		result_bots_end = self.__get_mongo_aggregate("users", query_bots_end, params['end']['Bot'])

		result = self.__insert_info_list(result, result_tweets_start, keep_track_places)
		result = self.__insert_info_list(result, result_users_start, keep_track_places)
		result = self.__insert_info_list(result, result_bots_start, keep_track_places)

		result = self.__insert_info_list(result, result_tweets_interm, keep_track_places)
		result = self.__insert_info_list(result, result_users_interm, keep_track_places)
		result = self.__insert_info_list(result, result_bots_interm, keep_track_places)

		result = self.__insert_info_list(result, result_tweets_end, keep_track_places)
		result = self.__insert_info_list(result, result_users_end, keep_track_places)
		result = self.__insert_info_list(result, result_bots_end, keep_track_places)

		logger.debug("It took " + str(time()-start))

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
					json.dump(result, file, indent=3)
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
