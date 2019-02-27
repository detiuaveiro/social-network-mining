from neo4j import Driver
from neo4j import GraphDatabase
from neo4j import Session

from interfaces import Storage


class Neo4JWrapper(Storage):

    @staticmethod
    def connect(**parameters):
        URI = parameters.pop("uri")
        AUTH = (parameters.pop("user"), parameters.pop("password"))
        return GraphDatabase.driver(URI, auth=AUTH)

    def __init__(self, **options):
        self._con: Driver = Neo4JWrapper.connect(**options)
        self._session: Session = self._con.session()

    def close(self):
        self._session.close()
        self._con.close()
