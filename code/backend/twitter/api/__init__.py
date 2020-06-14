from wrappers.neo4j_wrapper import Neo4jAPI
import os

NEO4J_PORT = os.environ.get('NEO4J_PORT', None)

if NEO4J_PORT:
    FULL_URL = f'neo4j:{NEO4J_PORT}'
    neo4j = Neo4jAPI(FULL_URL)
else:
    neo4j = Neo4jAPI()


