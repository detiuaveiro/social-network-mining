from wrappers.neo4j_wrapper import Neo4jAPI
import json

neo = Neo4jAPI()


def create_node(data):
	if data["labels"][0] == "Bot":
		if not neo.check_bot_exists(data["properties"]["id"]):
			neo.add_bot(data["properties"])
	if data["labels"][0] == "User":
		if not neo.check_user_exists(data["properties"]["id"]):
			neo.add_user(data["properties"])
	if data["labels"][0] == "Tweet":
		if not neo.check_tweet_exists(data["properties"]["id"]):
			neo.add_tweet(data["properties"])

def create_rel(rel, data):
	create_node(data["r"]["rels"][0]["start"])
	create_node(data["r"]["rels"][0]["end"])

	if rel=="FOLLOWS":
		rel = {
			"id_1": data["r"]["rels"][0]["start"]["properties"]["id"],
			"id_2": data["r"]["rels"][0]["end"]["properties"]["id"],
			"type_1": data["r"]["rels"][0]["start"]["labels"][0],
			"type_2": data["r"]["rels"][0]["end"]["labels"][0]
		}
		neo.add_follow_relationship(rel)
	elif rel == "REPLIED":
		rel = {
			"reply": data["r"]["rels"][0]["start"]["properties"]["id"],
			"tweet": data["r"]["rels"][0]["end"]["properties"]["id"],
		}
		neo.add_reply_relationship(rel)
	elif rel == "QUOTED":
		rel = {
			"tweet_id": data["r"]["rels"][0]["start"]["properties"]["id"],
			"quoted_tweet": data["r"]["rels"][0]["end"]["properties"]["id"],
		}
		neo.add_quote_relationship(rel)
	elif rel == "RETWEETED":
		rel = {
			"tweet_id": data["r"]["rels"][0]["end"]["properties"]["id"],
			"user_id": data["r"]["rels"][0]["start"]["properties"]["id"],
			"user_type": data["r"]["rels"][0]["start"]["labels"][0],
		}
		neo.add_retweet_relationship(rel)
	elif rel == "WROTE":
		rel = {
			"tweet_id": data["r"]["rels"][0]["end"]["properties"]["id"],
			"user_id": data["r"]["rels"][0]["start"]["properties"]["id"],
			"user_type": data["r"]["rels"][0]["start"]["labels"][0],
		}
		neo.add_writer_relationship(rel)


with open("export/follow2k.json", "r") as f:
	while True:
		line = f.readline()
		if not line:
			break
		create_rel("FOLLOWS", json.loads(line))

print("Done follows")

with open("export/replied2k.json", "r") as f:
	while True:
		line = f.readline()
		if not line:
			break
		create_rel("REPLIED", json.loads(line))

print("Done replies")

with open("export/quoted2k.json", "r") as f:
	while True:
		line = f.readline()
		if not line:
			break
		create_rel("QUOTED", json.loads(line))

print("Done quotes")

with open("export/retweeted2k.json", "r") as f:
	while True:
		line = f.readline()
		if not line:
			break
		create_rel("RETWEETED", json.loads(line))

print("Done retweet")

with open("export/wrote2k.json", "r") as f:
	while True:
		line = f.readline()
		if not line:
			break
		create_rel("WROTE", json.loads(line))

print("Done wrote")

neo.close()