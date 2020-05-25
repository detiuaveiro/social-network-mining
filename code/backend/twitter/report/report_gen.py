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


class Exporter:
	def __init__(self, directory):
		self.directory = directory

		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

	def export_csv(self, result):
		try:
			if len(result) == 0:
				return None

			headers = [key + "_" + prop for key in result[0] for prop in result[0][key]]
			file_dir = f"{self.directory}/export.csv"
			with open(file_dir, 'w') as file:
				writer = csv.writer(file, quotechar='"', escapechar='\\')
				writer.writerow(headers)
				for data in result:
					writer.writerow([str(data[key][prop]).encode('unicode_escape').decode('latin-1')
									 for key in data for prop in data[key]])
			return file_dir
		except Exception as error:
			logger.exception(f"Occurred an error <{error}>: ")
			return None

	def export_json(self, result):
		file_dir = f"{self.directory}/export.json"
		try:
			with open(file_dir, "w") as file:
				json.dump(result, file, indent=3)
			return file_dir
		except Exception as error:
			logger.exception(f"Occurred an error <{error}>: ")
			return None


class Report:
	mongo = MongoAPI()
	NEO4J_PORT = os.environ.get('NEO4J_PORT', None)

	if NEO4J_PORT:
		FULL_URL = f'neo4j:{NEO4J_PORT}'
		neo4j = Neo4jAPI(FULL_URL)
	else:
		neo4j = Neo4jAPI()

	exporter = Exporter(EXPORT_DIR)

	@staticmethod
	def translate_params(parameters):
		parameters = {key: [TRANSLATE[param] for param in parameters[key]] for key in parameters}
		return parameters

	@staticmethod
	def node_builder(label, node):
		query_node = "("
		if label:
			query_node += f":{label}"
		if node and len(node) > 0:
			query_node += f"{{id: '{node}'}}"

		return query_node+")"

	@staticmethod
	def relation_builder(rel, dir):
		if not rel:
			return "-[]->"
		query_rel = "["
		if len(rel) > 0:	#Its been hell dude
			if 'label' in rel:
				query_rel += ":" + '|'.join(rel['label'])
			if 'depth_start' in rel:
				query_rel += "*" + str(rel['depth_start'])
			if 'depth_end' in rel:
				query_rel += ".."+str(rel['depth_end'])
		query_rel += "]"

		if not dir or dir == NORMAL_REL:
			return f"-{query_rel}->"
		elif dir == REVERSE_REL:
			return f"<-{query_rel}-"
		return f"-{query_rel}-"

	@staticmethod
	def get_mongo_info(node, params):
		node_type = node["labels"][0]

		if node_type in params and len(params[node_type]) > 0:
			if node_type == TWEET_LABEL:
				mongo_info = Report.mongo.search('tweets', query={"id_str": node['properties']['id']},
										 fields=params[node_type], single=True)
			# It's a user or a bot
			else:
				mongo_info = Report.mongo.search('users', query={"id_str": node['properties']['id']},
											 fields=params[node_type], single=True)
			if mongo_info:
				return mongo_info
			return {param: None for param in params[node_type]}
		return None

	@staticmethod
	def get_mongo_aggregate(table, query, params):
		params += ["id_str"]
		if len(query) > 0 and len(params) > 0:
			result = Report.mongo.search(table, query={"$or": [{"id_str": obj_id} for obj_id in query]}, fields=params)
			return result
		return None

	@staticmethod
	def insert_info_list(info_dict, results_list, placement_dict, label=None):
		if results_list:
			for result in results_list:
				for index, key in placement_dict[result["id_str"]]:
					if label:
						result["label"] = label
					info_dict[index][key] = result
		return info_dict

	@staticmethod
	def query_builder(query, node):
		node_label = node["labels"][0]
		if node_label == TWEET_LABEL:
			query["Tweet"].append(node["properties"]["id"])
		elif node_label == USER_LABEL:
			query["User"].append(node["properties"]["id"])
		elif node_label == BOT_LABEL:
			query["Bot"].append(node["properties"]["id"])

	@staticmethod
	def get_results(result, query, placement, params):
		result_tweets = Report.get_mongo_aggregate("tweets", query['Tweet'], params['Tweet'])
		result = Report.insert_info_list(result, result_tweets, placement, label='Tweet')

		result_users = Report.get_mongo_aggregate("users", query['User'], params['User'])
		result = Report.insert_info_list(result, result_users, placement, label='User')

		result_bots = Report.get_mongo_aggregate("users", query['Bot'], params['Bot'])
		result = Report.insert_info_list(result, result_bots, placement, label='Bot')

		return result
	
	@staticmethod
	def add_to_keep_track(locations_dict, node, location):
		if node not in locations_dict:
			locations_dict[node] = []
		locations_dict[node].append(location)

	@staticmethod
	def neo_query_builder(match: dict, limit=None):
		query = "MATCH r="
		if ("relation" in match['start'] and match['start']['relation']) \
				or ('type' in match['start'] and match['start']['type']) \
				or ('node' in match['start'] and match['start']['node']):
			if 'node' not in match['start']:
				match['start']['node'] = None
			if 'direction' not in match['start']:
				match['start']['direction'] = None
			query += f"{Report.node_builder(match['start']['type'], match['start']['node'])}" \
					 f"{Report.relation_builder(match['start']['relation'], match['start']['direction'])}"

		if "intermediates" in match:
			intermediates = match["intermediates"]
			for interm in range(len(intermediates["types"])):
				query += f"{Report.node_builder(intermediates['types'][interm], intermediates['nodes'][interm])}" \
						 f"{Report.relation_builder(intermediates['relations'][interm])}"

		query += f"{Report.node_builder(match['end']['type'], match['end']['node'])} " \
				 f"return r"

		if limit:
			query += f" limit {limit}"

		logger.debug(query)

		return query

	@staticmethod
	def create_report(match: dict, params: dict, limit=None, export="csv"):
		params = Report.translate_params(params)

		query = Report.neo_query_builder(match, limit)

		result = []

		start = time()

		query_result = Report.neo.export_query(query, rel_node_properties=True)

		logger.info(f"It took <{time() - start}>s to get the network")

		query_for_mongo = {key: [] for key in params}

		keep_track_places = {}

		for row_index in range(len(query_result)):
			# Analyse each row by looking at its rels field
			row = query_result[row_index]
			relations = row['r']['rels']
			relation = {}

			# Add the detailed start node
			if len(relations) > 0:
				node_start = relations[0]["start"]
				Report.query_builder(query_for_mongo, node_start)
				Report.add_to_keep_track(keep_track_places, node_start["properties"]["id"], (row_index, "start"))
				relation["start"] = {param: None for param in params[node_start["labels"][0]]}
				relation["start"]["id_str"] = node_start["properties"]["id"]
				relation["start"]["label"] = node_start["labels"][0]

			for index in range(len(relations) - 1):
				rel = relations[index]
				relation['rel' + str(index+1)] = {"name": rel["label"]}
				Report.query_builder(query_for_mongo, rel["end"])
				Report.add_to_keep_track(keep_track_places, rel["end"]["properties"]["id"],
									(row_index, "interm" + str(index + 1)))
				relation["interm" + str(index+1)] = {param: None for param in params[rel["end"]["labels"][0]]}
				relation["interm" + str(index + 1)]["id_str"] = rel["end"]["properties"]["id"]
				relation["interm" + str(index + 1)]["label"] = rel["end"]["labels"][0]

			# Add ending node
			if len(relations) > 0:
				relation['rel' + str(len(relations))] = {"name": relations[-1]["label"]}
			node_end = row['r']['nodes'][-1]
			Report.query_builder(query_for_mongo, node_end)
			Report.add_to_keep_track(keep_track_places, node_end["properties"]["id"], (row_index, "end"))
			relation["end"] = {param: None for param in params[node_end["labels"][0]]}
			relation["end"]["id_str"] = node_end["properties"]["id"]
			relation["end"]["label"] = node_end["labels"][0]

			# Append to result
			result.append(relation)

		logger.debug(f"It took <{time() - start} s> to finish analysing network")

		result = Report.get_results(result, query_for_mongo, keep_track_places, params)

		logger.debug(f"It took <{time() - start} s>")

		if export == "csv":
			return Report.exporter.export_csv(result)
		elif export == "json":
			return Report.exporter.export_json(result)


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

	Report.create_report(query2, params, limit=5000, export=Report.ExportType.CSV)
#
#
#
# 	test_report(query, params, limit)
# 	test_report(query, params, limit, "json")
