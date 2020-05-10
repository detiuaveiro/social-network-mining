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


EXPORT_DIR = "../export"
NORMAL_REL = 'Normal'
REVERSE_REL = 'Reverse'
TRANSLATE = {
	"b_name": "name", "b_username": "screen_name", "b_location": "location", "b_description": "description",
	"b_tweets": "status_count", "b_followers": "followers_count", "b_following": "friends_count",
	"b_protected": "protected", "u_name": "name", "u_username": "screen_name", "u_location": "location",
	"u_description": "description", "u_tweets": "status_count", "u_followers": "followers_count",
	"u_following": "friends_count",	"u_protected": "protected", "t_creation": "created_at", "t_text": "text",
	"t_lang": "lang", "t_noRetweets": "retweet_count", "t_noLikes": "favourite_count",
	"t_sensitive": "possibly_sensitive"
}


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

	def __translate_params(self, parameters):
		parameters = {key: [TRANSLATE[param] for param in parameters[key]] for key in parameters}
		return parameters

	#@staticmethod
	def __node_builder(self, label, node):
		query_node = "("
		if label:
			query_node += f":{label}"
		if node and len(node) > 0:
			query_node += f"{{id: '{node[0]}'}}"

		return query_node+")"

	#@staticmethod
	def __relation_builder(self, rel):
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

	#@staticmethod
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

	#@staticmethod
	def __get_mongo_aggregate(self, table, query, params):
		params += ["id_str"]
		if len(query) > 0 and len(params) > 0:
			result = self.mongo.search(table, query={"$or": [{"id_str": obj_id} for obj_id in query]}, fields=params)
			return result
		return None

	#@staticmethod
	def __insert_info_list(self, info_dict, results_list, placement_dict):
		if results_list:
			for result in results_list:
				for index, key in placement_dict[result["id_str"]]:
					info_dict[index][key] = result
		return info_dict

	#@staticmethod
	def __query_builder(self, query, node):
		node_label = node["labels"][0]
		if node_label == TWEET_LABEL:
			query["Tweet"].append(node["properties"]["id"])
		elif node_label == USER_LABEL:
			query["User"].append(node["properties"]["id"])
		elif node_label == BOT_LABEL:
			query["Bot"].append(node["properties"]["id"])

	#@staticmethod
	def __get_results(self, result, query, placement, params):
		result_tweets = self.__get_mongo_aggregate("tweets", query['Tweet'], params['Tweet'])

		result_users = self.__get_mongo_aggregate("users", query['User'], params['User'])

		result_bots = self.__get_mongo_aggregate("users", query['Bot'], params['Bot'])

		for res in [result_tweets, result_users, result_bots]:
			result = self.__insert_info_list(result, res, placement)

		return result

	#@staticmethod
	def __add_to_keep_track(self, locations_dict, node, location):
		if node not in locations_dict:
			locations_dict[node] = []
		locations_dict[node].append(location)

	#@staticmethod
	def create_report(self, match: dict, params: dict, limit=None):
		params = self.__translate_params(params)
		query = "MATCH r="
		if "relation" in match['start']:
			query += f"{self.__node_builder(match['start']['type'], match['start']['node'])}" \
					f"{self.__relation_builder(match['start']['relation'])}"

		if "intermediates" in match:
			intermediates = match["intermediates"]
			for interm in range(len(intermediates["types"])):
				query += f"{self.__node_builder(intermediates['types'][interm], intermediates['nodes'][interm])}" \
						f"{self.__relation_builder(intermediates['relations'][interm])}"

		query += f"{self.__node_builder(match['end']['type'], match['end']['node'])} " \
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
			relation["start"]["id_str"] = node_start["properties"]["id"]
			relation["start"]["label"] = node_start["labels"][0]

			for index in range(len(relations) - 1):
				rel = relations[index]
				relation['rel' + str(index+1)] = {"name": rel["label"]}
				self.__query_builder(query_for_mongo, rel["end"])
				self.__add_to_keep_track(keep_track_places, rel["end"]["properties"]["id"],
										 (row_index, "interm" + str(index + 1)))
				relation["interm" + str(index+1)] = {param: None for param in params[rel["end"]["labels"][0]]}
				relation["interm" + str(index + 1)]["id_str"] = rel["end"]["properties"]["id"]
				relation["interm" + str(index + 1)]["label"] = rel["end"]["labels"][0]

			# Add ending node
			relation['rel' + str(len(relations))] = {"name": relations[-1]["label"]}
			node_end = relations[-1]["end"]
			self.__query_builder(query_for_mongo, node_end)
			self.__add_to_keep_track(keep_track_places, node_end["properties"]["id"], (row_index, "end"))
			relation["end"] = {param: None for param in params[node_end["labels"][0]]}
			relation["end"]["id_str"] = node_end["properties"]["id"]
			relation["end"]["label"] = node_end["labels"][0]

			# Append to result
			result.append(relation)

		logger.debug(f"It took <{time() - start} s> to finish analysing network")

		result = self.__get_results(result, query_for_mongo, keep_track_places, params)

		logger.debug(f"It took <{time() - start} s>")

		#if export == self.ExportType.CSV:
		#	self.exporter.export_csv(result)
		#elif export == self.ExportType.JSON:
		#	self.exporter.export_json(result)
		return result

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

	for export_type in Report.ExportType:
		print(export_type)
		rep.create_report(query, params, export=export_type)

	# Test intermediates
	query = {
		"match": {
			"start": {
				"node": {
					"label": "User"
				},
				"relation": {
					"label": ["WROTE"]
				}
			},
			"intermediates": [
				{
					"node": {
						"label": "Tweet"
					},
					"relation": {
						"label": ["RETWEETED", "QUOTED", "REPLIED"],
						"direction": "Reverse"
					}
				}
			],
			"end": {
				"node": {
					"label": "User"
				}
			}
		},
		"fields": {
			"Tweet": ["retweet_count", "favourite_count", "text", "id_str"],
			"User": ["name", "screen_name", "followers_count", "id_str"],
			"Bot": ["name", "screen_name", "friends_count", "id_str"]
		},
		"limit": None
	}

	for export_type in Report.ExportType:
		print(export_type)
		rep.create_report(query2, params, export=export_type)
#
#
#
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
