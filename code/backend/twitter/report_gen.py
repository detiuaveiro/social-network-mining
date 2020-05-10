import os
import csv
import json
import logging
from enum import IntEnum
from time import time

from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI
from neo4j_labels import USER_LABEL, BOT_LABEL, TWEET_LABEL


logger = logging.getLogger("report")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("report_gen.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


EXPORT_DIR = "export"
NORMAL_REL = 'Normal'
REVERSE_REL = 'Reverse'


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
				query_node += ":" + node['label']
			if 'screen_name' in node:
				query_node += f"{{username:'{node['screen_name']}'}}"

		return query_node+")"

	@staticmethod
	def __relation_builder(rel):
		query_rel = "["
		if len(rel) > 0:
			if 'label' in rel:
				query_rel += ":" + '|'.join(rel['label'])
			if 'depth_start' in rel:
				query_rel += "*" + str(rel['depth_start'])
			if 'depth_end' in rel:
				query_rel += ".."+str(rel['depth_end'])
		query_rel += "]"
		if "direction" not in rel or rel["direction"] == NORMAL_REL:
			return f"-{query_rel}->"
		elif rel["direction"] == REVERSE_REL:
			return f"<-{query_rel}-"
		return f"-{query_rel}-"

	def __get_mongo_info(self, node, params):
		node_type = node["labels"][0]

		if node_type in params and len(params[node_type]) > 0:

			if node_type == TWEET_LABEL:
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
	def __insert_info_list(info_dict, results_list, placement_dict, label=None):
		if results_list:
			for result in results_list:
				for index, key in placement_dict[result["id_str"]]:
					if label:
						result["label"] = label
					info_dict[index][key] = result
		return info_dict

	def __query_builder(self, query, node):
		node_label = node["labels"][0]
		if node_label == TWEET_LABEL:
			query["Tweet"].append(node["properties"]["id"])
		elif node_label == USER_LABEL:
			query["User"].append(node["properties"]["id"])
		elif node_label == BOT_LABEL:
			query["Bot"].append(node["properties"]["id"])

	def __get_results(self, result, query, placement, params):
		result_tweets = self.__get_mongo_aggregate("tweets", query['Tweet'], params['Tweet'])
		result = self.__insert_info_list(result, result_tweets, placement, label='Tweet')

		result_users = self.__get_mongo_aggregate("users", query['User'], params['User'])
		result = self.__insert_info_list(result, result_users, placement, label='User')

		result_bots = self.__get_mongo_aggregate("users", query['Bot'], params['Bot'])
		result = self.__insert_info_list(result, result_bots, placement, label='Bot')

		return result
	
	def __add_to_keep_track(self, locations_dict, node, location):
		if node not in locations_dict:
			locations_dict[node] = []
		locations_dict[node].append(location)

	def create_report(self, match: dict, params: dict, limit=None, export=ExportType.CSV):
		query = f"MATCH r={self.__node_builder(match['start']['node'])}" \
				f"{self.__relation_builder(match['start']['relation'])}"

		if "intermediates" in match:
			for interm in match["intermediates"]:
				query += f"{self.__node_builder(interm['node'])}" \
						f"{self.__relation_builder(interm['relation'])}"

		query += f"{self.__node_builder(match['end']['node'])} " \
				 f"return r"

		logger.info(query)
		
		if limit:
			query += f" limit {limit}"

		result = []

		start = time()

		query_result = self.neo.export_query(query, rel_node_properties=True)

		logger.info(f"It took <{time() - start}>s to get the network")
		self.exporter.export_json(query_result)

		query_for_mongo = {key: [] for key in params}

		keep_track_places = {}

		for row_index in range(len(query_result)):
			# Analyse each row by looking at its rels field
			row = query_result[row_index]
			relations = row['r']['rels']
			relation = {}

			# Add the detailed start node
			node_start = relations[0]["start"]
			self.__query_builder(query_for_mongo, node_start)
			self.__add_to_keep_track(keep_track_places, node_start["properties"]["id"], (row_index, "start"))
			relation["start"] = {param: None for param in params[node_start["labels"][0]]}

			for index in range(len(relations) - 1):
				rel = relations[index]
				relation['rel' + str(index+1)] = {"name": rel["label"]}
				self.__query_builder(query_for_mongo, rel["end"])
				self.__add_to_keep_track(keep_track_places, rel["end"]["properties"]["id"],
										 (row_index, "interm" + str(index + 1)))
				relation["interm" + str(index+1)] = {param: None for param in params[rel["end"]["labels"][0]]}

			# Add ending node
			relation['rel' + str(len(relations))] = {"name": relations[-1]["label"]}
			node_end = relations[-1]["end"]
			self.__query_builder(query_for_mongo, node_end)
			self.__add_to_keep_track(keep_track_places, node_end["properties"]["id"], (row_index, "end"))
			relation["end"] = {param: None for param in params[node_end["labels"][0]]}

			# Append to result
			result.append(relation)

		logger.debug(f"It took <{time() - start} s> to finish analysing network")

		result = self.__get_results(result, query_for_mongo, keep_track_places, params)

		logger.debug(f"It took <{time() - start} s>")

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
					writer = csv.writer(file, quotechar='"', escapechar='\\')
					writer.writerow(headers)
					for data in result:
						writer.writerow([str(data[key][prop]).encode('unicode_escape').decode('latin-1')
						                 for key in data for prop in data[key]])
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
		'start': {
			'node': {
				'label': "User"
			},
			'relation': {
				'label': ['FOLLOWS']
			}
		},
		'end': {
			'node': {
				'screen_name': 'KimKardashian',
				'label': "User"
			}
		}
	}
	params = {
		'Tweet': ['retweet_count', 'favourite_count', 'text', "id_str"],
		'User': ['name', 'screen_name', 'followers_count', "id_str"],
		'Bot': ['name', 'screen_name', 'friends_count', "id_str"]
	}

	#for export_type in Report.ExportType:
	#	print(export_type)
	#	rep.create_report(query, params, export=export_type)

	# Test intermediates
	query2 = {
		'start': {
			'node': {},
			'relation': {
				'direction': 'Bidirectional'
			}
		},
		'end': {
			'node': {}
		}
	}

	rep.create_report(query2, params, limit=5000, export=Report.ExportType.CSV)
#
#
#
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
