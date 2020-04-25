from wrappers import neo4j_wrapper as neo
import json

neo4j = neo.Neo4jAPI()

with open("network.json", "w") as f:
	json.dump(neo4j.export_sample_network(), f)