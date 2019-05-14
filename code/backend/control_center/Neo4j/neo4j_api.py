from neo4j import GraphDatabase
from enum import IntEnum

class Neo4jTypes(IntEnum):
    CREATE_BOT = 1
    CREATE_USER = 2
    CREATE_RELATION = 3
    SEARCH_USER = 4
    UPDATE_USER = 5
    SEARCH_BOT = 6
    UPDATE_BOT = 7

class Neo4jAPI():
    def __init__(self):
        print("Creating connection")
        self._driver = GraphDatabase.driver("bolt://192.168.85.187:7687",auth=("neo4j","neo4jPI"))

    def close(self):
        self._driver.close()

    def task(self, query_type, data):
        print("Iniciating Session")
        with self._driver.session() as session:
            if (query_type==Neo4jTypes.CREATE_BOT):
                session.write_transaction(self.create_bot, data)
            elif (query_type==Neo4jTypes.CREATE_USER):
                session.write_transaction(self.create_user, data)
            elif (query_type==Neo4jTypes.CREATE_RELATION):
                session.write_transaction(self.create_relationship, data)
            elif (query_type==Neo4jTypes.SEARCH_USER):
                result = session.write_transaction(self.search_user, data)
                return result
            elif (query_type==Neo4jTypes.UPDATE_USER):
                session.write_transaction(self.update_user, data)
            elif (query_type==Neo4jTypes.SEARCH_BOT):
                result = session.write_transaction(self.search_bot, data)
                return result
            elif (query_type==Neo4jTypes.UPDATE_BOT):
                session.write_transaction(self.update_bot, data)           

    @staticmethod
    def create_bot(tx, data):
        print("NEO4J: TASK CREATE BOT")
        bot_name = data['name']
        bot_id = data['id']
        bot_username = data['username']
        print("Query to create bot")
        result = tx.run("CREATE (:Bot { name: $name, id: $id, username: $username })", id=bot_id, name=bot_name,  username=bot_username)

    @staticmethod
    def create_user(tx, data):
        print("NEO4J: TASK CREATE USER")
        user_name = data['name']
        user_id = data['id']
        user_username = data['username']
        print("Query to create user")
        result = tx.run("CREATE (:User { name: $name, id: $id, username: $username })", id=user_id, name=user_name, username=user_username)
    
    
    @staticmethod
    def create_relationship(tx, data):
        print("NEO4J: TASK CREATE RELATION")
        bot_id = data['bot_id']
        user_id = data['user_id']
        print("Query to create relation between two nodes")
        result = tx.run("MATCH (u:Bot { id: $bot_id }), (r:User {id:$user_id}) \
                        CREATE (u)-[:FOLLOWS]->(r)", bot_id=bot_id, user_id=user_id)

    @staticmethod
    def search_user(tx, data):
        print("NEO4J: TASK SEARCH USER")
        user_id = data['user_id']
        result = tx.run("MATCH (r:User { id:$id }) \
                        RETURN r", id=user_id)
<<<<<<< HEAD
=======
        print(result.data())
>>>>>>> RESTRUCTURE
        if (len(result.data())==0):
            return False
        else:
            return True
    
    @staticmethod
    def search_bot(tx, data):
        print("NEO4J: TASK SEARCH BOT")
        bot_id = data['bot_id']
        result = tx.run("MATCH (r:Bot { id:$id }) \
                        RETURN r", id=bot_id)
<<<<<<< HEAD
=======
        print(result.data())
>>>>>>> RESTRUCTURE
        if (len(result.data())==0):
            return False
        else:
            return True
    
    @staticmethod
    def update_user(tx, data):
        print("NEO4J: TASK UPDATE USER")
        user_id = data['user_id']
        user_name = data['user_name']
        user_username = data['user_username']
        print("Query to update user")
        result = tx.run("MATCH (r:User { id:$id }) \
                        SET r = { id: $id, name: $name, username: $username } \
                        RETURN r", id=user_id, name=user_name, username=user_username)

    @staticmethod
    def update_bot(tx, data):
        print("NEO4J: TASK UPDATE BOT")
        bot_id = data['bot_id']
        bot_name = data['bot_name']
        bot_username = data['bot_username']
        print("Query to update user")
        result = tx.run("MATCH (r:Bot { id:$id }) \
                        SET r = { id: $id, name: $name, username: $username } \
                        RETURN r", id=bot_id, name=bot_name, username=bot_username)