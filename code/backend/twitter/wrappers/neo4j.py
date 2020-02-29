from neo4j import GraphDatabase
import logging
import sys

sys.path.append("..")
import credentials

log = logging.getLogger("Neo4j")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class NeoAPI:
    """Neo4j Wrapper.

    Class that acts as a wrapper for all methods related to our Neo4j DB 
    """

    def __init__(self):
        log.debug("Connecting to Neo4j")
        self.client = GraphDatabase.driver(
            "bolt://" + credentials.NEO4J_FULL_URL,
            auth=(credentials.NEO4J_USERNAME, credentials.NEO4J_PASSWORD),
        )

    def close(self):
        self._client.close()
