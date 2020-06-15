from pymongo import MongoClient
from neo4j import GraphDatabase
import os

mongo = MongoClient("mongodb://localhost:27017")
users = eval(f"mongo.twitter.users")

FULL_URL = f"{os.environ.get('NEO4J_URL', 'localhost')}:7687"
NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'neo4jPI')

neo4j = GraphDatabase.driver(
			"bolt://" + FULL_URL,
			auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False
		)


def add_protected():
	with neo4j.session() as session:
		session.run("Match (n :User) SET n.protected = false return n")
	user_list = users.find({"protected": True})
	for user in user_list:
		with neo4j.session() as session:
			session.run("MATCH (n {id: $id}) SET n.protected = true return n",
						id=user['id_str'])
	print("Done")


if __name__ == "__main__":
	add_protected()
