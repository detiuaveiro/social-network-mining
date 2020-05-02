from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI
import csv
import json


def export_csv(result):
	csv_file = "export.csv"
	headers = [key + "_" + prop for key in result[0] for prop in result[0][key]]
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(headers)
			for data in result:
				writer.writerow([data[key][prop] for key in data for prop in data[key]])
	except IOError:
		print("I/O error")


def export_json(result):
	with open("export.json", "w") as jsonfile:
		json.dump(result, jsonfile)


def test_report(query, params={}, limit=None, export='csv'):
	mongo = MongoAPI()
	neo = Neo4jAPI()
	query += "return " + ",".join(params.keys())
	if limit is not None:
		query += " limit " + str(limit)
	result = []
	for row in neo.export_query(query):
		row_dict = {}
		for key in row:
			if type(row[key]) is dict and row[key]['type'] == "node":
				if row[key]['labels'] == ['Tweet']:
					row_dict[key] = mongo.search(
						'tweets', query={"id_str": row[key]['properties']['id']}, fields=params[key], single=True)
					if not row_dict[key]:
						row_dict[key] = {prop: None for prop in params[key]}
				else:
					row_dict[key] = mongo.search(
						'users', query={"id_str": row[key]['properties']['id']}, fields=params[key], single=True)
					if not row_dict[key]:
						row_dict[key] = {prop: None for prop in params[key]}
		result.append(row_dict)

	if export == 'csv':
		export_csv(result)
	elif export == 'json':
		export_json(result)


if __name__ == '__main__':
	query = "MATCH (a: Tweet) - [r] - (b: User)"
	params = {
		'a': ['retweet_count', 'favorite_count'],
		'b': ['name', 'screen_name', 'statuses_count'],
		'r': []
	}
	limit = 5
	test_report(query, params, limit)
	test_report(query, params, limit, "json")

