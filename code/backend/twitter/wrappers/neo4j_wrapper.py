import logging
import sys
from neo4j import GraphDatabase
import datetime
sys.path.append('..')
import credentials

log = logging.getLogger("Neo4j")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)

BOT_LABEL = "Bot"
USER_LABEL = "User"
FOLLOW_LABEL = "FOLLOWS"


class Neo4jAPI:
    def __init__(self):
        log.debug("Connecting to Neo4j")
        self.driver = GraphDatabase.driver(
            "bolt://" + credentials.NEO4J_FULL_URL,
            auth=(credentials.NEO4J_USERNAME, credentials.NEO4J_PASSWORD),
        )

    def close(self):
        self.driver.close()

    def add_bot(self, data):
        """Method used to create a new bot

        @param data: The params of the new bot we want to create. Should include an id, name and username
        """
        if (
                "id" not in data.keys()
                or "name" not in data.keys()
                or "username" not in data.keys()
        ):
            log.error("ERROR CREATING A BOT")
            log.error(
                "Error: Specified data doesn't contain necessary fields - id, name, username"
            )

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__create_bot, data)

    def __create_bot(self, tx, data):
        log.debug("CREATING BOT")

        # Note we use Merge rather than Create to avoid duplicates
        tx.run(
            f"MERGE (:{BOT_LABEL} {{ name: $name, id: $id, username: $username }} )",
            id=data["id"],
            name=data["name"],
            username=data["username"],
        )

    def add_user(self, data):
        """Method used to create a new user

        @param data: The params of the new bot we want to create. Should include an id, name and username
        """
        if (
                "id" not in data.keys()
                or "name" not in data.keys()
                or "username" not in data.keys()
        ):
            log.error("ERROR CREATING A USER")
            log.debug(
                "Error: Specified data doesn't contain necessary fields - id, name, username"
            )

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__create_user, data)

    def __create_user(self, tx, data):
        log.debug("CREATING USER")

        tx.run(
            f"MERGE (:{USER_LABEL} {{ name: $name, id: $id, username: $username }})",
            id=data["id"],
            name=data["name"],
            username=data["username"],
        )

    def add_relationship(self, data):
        """Method used to create a new FOLLOWS relationship

        @param data: The params of the new relationship we want to create. Should include a type_1, type_2, id_1, id_2
        """
        if (
                "id_1" not in data.keys()
                or "id_2" not in data.keys()
                or "type_1" not in data.keys()
                or "type_2" not in data.keys()
        ):
            log.error("ERROR CREATING A RELATIONSHIP")
            log.error(
                "Error: Specified data doesn't contain necessary fields - type_1, type_2, id_1, id_2"
            )

            return

        if data["type_1"] not in [BOT_LABEL, USER_LABEL] or data["type_2"] not in [
            BOT_LABEL,
            USER_LABEL,
        ]:
            log.error("ERROR CREATING A RELATIONSHIP")
            log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__create_relationship, data)

    def __create_relationship(self, tx, data):
        log.debug("CREATING RELATIONSHIP")

        query = f'MATCH (u: {data["type_1"]} {{ id: {str(data["id_1"])} }}), ' \
                f'(r: {data["type_2"]} {{ id: {str(data["id_2"])} }}) MERGE (u)-[:{FOLLOW_LABEL}]->(r)'

        tx.run(query)

    def check_bot_exists(self, id):
        """Method used to check if there exists a bot with a given id

        @param id: The id of the bot we want to check the existance of
        """

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__bot_exists, id)

    def __bot_exists(self, tx, data):
        log.debug("CHECKING BOT EXISTANCE")

        result = tx.run(f"MATCH (r:{BOT_LABEL} {{ id:$id }}) RETURN r", id=data)

        if len(result.data()) == 0:
            return False
        else:
            return True

    def check_user_exists(self, id):
        """Method used to check if there exists a user with a given id

        @param id: The id of the user we want to check the existance of
        """

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__user_exists, id)

    def __user_exists(self, tx, data):
        log.debug("CHECKING USER EXISTANCE")

        result = tx.run(f"MATCH (r:{USER_LABEL} {{ id:$id }}) RETURN r", id=data)

        if len(result.data()) == 0:
            return False
        else:
            return True

    def update_user(self, data):
        """Method used to update a given user

        @param data: The id of the user we want to update and the other update params. Should include an old_id
        """
        if "id" not in data.keys():
            log.error("ERROR CREATING A USER")
            log.error("Error: Specified data doesn't contain necessary fields - old_id")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__update_user, data)

    def __update_user(self, tx, data):
        log.debug("UPDATING USER")

        set_query = ""
        if len(data.keys()) > 1:
            set_query = "SET "

        if "username" in data.keys():
            set_query += "r.username = '" + data["username"] + "',"
        if "name" in data.keys():
            set_query += "r.name = '" + data["name"] + "',"

        query = f'MATCH (r: {USER_LABEL} {{ id : {str(data["id"])} }}) {set_query[:-1]} RETURN r'

        tx.run(query)

    def update_bot(self, data):
        """Method used to update a given bot

        @param data: The params of the bot we want to update and the other update params. Should include an old_id
        """
        if "id" not in data.keys():
            log.error("ERROR CREATING A USER")
            log.error("Error: Specified data doesn't contain necessary fields - old_id")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__update_bot, data)

    def __update_bot(self, tx, data):
        log.debug("UPDATING BOT")

        set_query = ""
        if len(data.keys()) > 1:
            set_query = "SET "

        if "username" in data.keys():
            set_query += "r.username = '" + data["username"] + "',"
        if "name" in data.keys():
            set_query += "r.name = '" + data["name"] + "',"

        query = f'MATCH (r:{BOT_LABEL} {{ id: {str(data["id"])} }}) {set_query[:-1]}  RETURN r'
        # Note we use set_query[:-1] in order to remove the final comma (,)

        tx.run(query)

    def search_bots(self, data={}):
        """Method used to search for a given bot

        @param data: The params of the bot we want to look for. By default we look for all bots
        """

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__search_bots, data)

    def __search_bots(self, tx, data):
        log.debug("SEARCHING BOTS")

        query_filters = "{"
        if "id" in data.keys():
            query_filters += "id: " + str(data["id"]) + ","
        if "name" in data.keys():
            query_filters += "name: '" + data["name"] + "',"
        if "username" in data.keys():
            query_filters += "username: '" + data["username"] + "',"
        query_filters += query_filters[:-1] + "}"

        query = f'MATCH (r:{BOT_LABEL} {query_filters}) RETURN r'

        result = []
        for i in tx.run(query):
            result.append(dict(i.items()[0][1]))

        return result

    def search_users(self, data={}):
        """Method used to search for a given user

        @param data: The params of the user we want to look for. By default we look for all users
        """

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__search_users, data)

    def __search_users(self, tx, data):
        log.debug("SEARCHING USERS")

        query_filters = "{"
        if "id" in data.keys():
            query_filters += "id: " + str(data["id"]) + ","
        if "name" in data.keys():
            query_filters += "name: '" + data["name"] + "',"
        if "username" in data.keys():
            query_filters += "username: '" + data["username"] + "',"
        query_filters = query_filters[:-1] + "}"

        query = f'MATCH (r:{USER_LABEL} {query_filters}) RETURN r'

        result = []
        for i in tx.run(query):
            result.append(dict(i.items()[0][1]))

        return result

    def check_relationship_exists(self, data):
        """Method used to check whether a relationship exists between two IDs

        @param data: The params of the entities involved in the relationshi+ we want to look for. Should include
            a type_1, type_2, id_1, id_2
        """
        if (
                "id_1" not in data.keys()
                or "id_2" not in data.keys()
                or "type_1" not in data.keys()
                or "type_2" not in data.keys()
        ):
            log.error("ERROR CHECKING RELATIONSHIP")
            log.debug(
                "Error: Specified data doesn't contain necessary fields - type_1, type_2, id_1, id_2"
            )

            return

        if data["type_1"] not in [BOT_LABEL, USER_LABEL] or data["type_2"] not in [
            BOT_LABEL,
            USER_LABEL,
        ]:
            log.error("ERROR CHECKING RELATIONSHIP")
            log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__check_relationship, data)

    def __check_relationship(self, tx, data):
        log.debug("VERIFYING RELATIONSHIP EXISTANCE")

        query = f'MATCH (a: {data["type_1"]} {{id: {str(data["id_1"])} }})-[r:{FOLLOW_LABEL}]' \
                f'->(b:{data["type_2"]} {{id: {str(data["id_2"])} }}) RETURN a, b'

        result = tx.run(query)

        if len(result.values()) == 0:
            return False
        else:
            return True

    def get_following(self, data):
        """Method used to find all accounts a given entity is following

        @param data: The specification of who we want to get the followings of. Should include a id and type
        """
        if "id" not in data.keys():
            log.error("ERROR RETRIEVING FOLLOWINGS")
            log.error(
                "Error: Specified data doesn't contain necessary fields - type, id"
            )

            return

        if 'type' in data and data["type"] not in [BOT_LABEL, USER_LABEL]:
            log.error("ERROR RETRIEVING FOLLOWINGS")
            log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__get_following, data)

    def __get_following(self, tx, data):
        log.debug("GETTING FOLLOWINGS")

        query = f"MATCH (a {':' + data['type'] if 'type' in data else ''} {{id: {str(data['id'])} }})-" \
                f"[r:{FOLLOW_LABEL}]->(b) RETURN b"

        result = []
        for i in tx.run(query):
            result.append(dict(i.items()[0][1]))

        return result

    def get_followers(self, data):
        """Method used to find all accounts following a given entity

        @param data: The specification of who we want to get the followings of. Should include a id and type
        """
        if "id" not in data.keys():
            log.error("ERROR RETRIEVING FOLLOWERS")
            log.debug(
                "Error: Specified data doesn't contain necessary fields - type, id"
            )

            return

        if 'type' in data and data["type"] not in [BOT_LABEL, USER_LABEL]:
            log.error("ERROR RETRIEVING FOLLOWINGS")
            log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__get_followers, data)

    def __get_followers(self, tx, data):
        log.debug("GETTING FOLLOWERS")

        query = f'MATCH (b)-[r:{FOLLOW_LABEL}]->' \
                f'(a {":" + data["type"] if "type" in data else ""} {{id: {str(data["id"])} }}) RETURN b'

        result = []
        for i in tx.run(query):
            result.append(dict(i.items()[0][1]))

        return result

    def export_network(self, export_type="graphml", export_name=None):
        """Method used to export the entire database

        @param export_type: What type we want to export to. Graphml by default
        @param export_name: The path we want to export to
        """

        if export_type not in ["json", "csv", "graphml"]:
            log.error("ERROR EXPORTING RESULT")
            log.error(
                "Error: ",
                "Specified export type not supported. Please use json, csv or graphml",
            )

            return

        if export_name is None:
            export_name = (
                "../export_results/"
                + export_type
                + "/neo4j"
                + "_"
                + str(datetime.datetime.now()).replace(" ", "_")
            )

            export_name = export_name + "." + export_type

        with self.driver.session() as session:
            return session.write_transaction(self.__export_network, {"type": export_type, "name": export_name})

    def __export_network(self, tx, data):
        log.debug("EXPORTING NETWORK")

        if data["type"] == "json":
            tx.run(
                "CALL apoc.export.json.all('" + data["name"] + "',{useTypes:true})"
            )
        elif data["type"] == "csv":
            tx.run(
                "CALL apoc.export.csv.all('" + data["name"] + "', {useTypes:true})"
            )
        else:
            tx.run("CALL apoc.export.graphml.all('" + data["name"] + "', {useTypes:true})")


if __name__ == "__main__":
    neo = Neo4jAPI()
    # neo.add_bot({"id":0,"name":"Jonas","username":"Jonas_Pistolas"})
    # neo.add_user({"id":0,"name":"DS","username":"FenixD.S"})
    # neo.add_relationship({"id_1": 0, "id_2": 0, "type_1": BOT_LABEL, "type_2": USER_LABEL})

    # print(neo.check_bot_exists(0))
    # print(neo.check_user_exists(0))

    # neo.update_user({"id": 0, "name": "Diogo Ass"})
    # neo.update_user({"id": 0, "username": "FenixDickSucker","name":"DS"})

    # neo.update_bot({"id":0,"name":"bot lindo"})

    # print(neo.search_bots({"name":"bot lindo"}))
    # print(neo.search_users({"id":0}))
    # print(neo.check_relationship_exists({"id_1": 0, "id_2": 0, "type_1": BOT_LABEL, "type_2": USER_LABEL}))

    # print(neo.get_following({"type": BOT_LABEL, "id": 0}))
    # print(neo.get_followers({"type": USER_LABEL, "id": 0}))

    # neo.export_network()
    # neo.export_network("csv")
    # neo.export_network("json")

    neo.close()
