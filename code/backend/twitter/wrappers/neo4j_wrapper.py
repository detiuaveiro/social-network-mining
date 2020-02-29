import logging
import sys
from neo4j import GraphDatabase

sys.path.append("..")
import credentials

log = logging.getLogger("Neo4j")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


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
            log.info("ERROR CREATING A BOT")
            log.debug(
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
            "MERGE (:BOT { name: $name, id: $id, username: $username })",
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
            log.info("ERROR CREATING A USER")
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
            "MERGE (:USER { name: $name, id: $id, username: $username })",
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
            or "id_1" not in data.keys()
            or "type_1" not in data.keys()
            or "type_2" not in data.keys()
        ):
            log.info("ERROR CREATING A RELATIONSHIP")
            log.debug(
                "Error: Specified data doesn't contain necessary fields - type_1, type_2, id_1, id_2"
            )

            return

        if data["type_1"] not in ["BOT", "USER"] or data["type_2"] not in [
            "BOT",
            "USER",
        ]:
            log.info("ERROR CREATING A RELATIONSHIP")
            log.debug("Error: Unaceptable specified types. Types must be BOT or USER")

            return

        with self.driver.session() as session:
            # Caller for transactional unit of work
            return session.write_transaction(self.__create_relationship, data)

    def __create_relationship(self, tx, data):
        log.debug("CREATING RELATIONSHIP")

        query = (
            "MATCH (u:"
            + data["type_1"]
            + " {id: "
            + str(data["id_1"])
            + " }), (r:"
            + data["type_2"]
            + " {id: "
            + str(data["id_2"])
            + "}) MERGE (u)-[:FOLLOWS]->(r)"
        )

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

        result = tx.run("MATCH (r:BOT { id:$id }) RETURN r", id=data)

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

        result = tx.run("MATCH (r:USER { id:$id }) RETURN r", id=data)

        if len(result.data()) == 0:
            return False
        else:
            return True


    def update_user(self, data):
        """Method used to update a given user

        @param data: The id of the user we want to update and the other update params. Should include an old_id
        """
        if "id" not in data.keys():
            log.info("ERROR CREATING A USER")
            log.debug("Error: Specified data doesn't contain necessary fields - old_id")

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

        query = (
            "MATCH (r:USER {id:" + str(data["id"]) + "}) " + set_query[:-1] + " RETURN r"
        )  # Note we use set_query[:-1] in order to remove the final comma (,)

        tx.run(query)


    def update_bot(self, data):
        """Method used to update a given bot

        @param data: The params of the bot we want to update and the other update params. Should include an old_id
        """
        if "id" not in data.keys():
            log.info("ERROR CREATING A USER")
            log.debug("Error: Specified data doesn't contain necessary fields - old_id")

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

        query = (
            "MATCH (r:BOT {id:" + str(data["id"]) + "}) " + set_query[:-1] + " RETURN r"
        )  # Note we use set_query[:-1] in order to remove the final comma (,)

        tx.run(query)


    def search_bots(self):
        pass


    def search_users(self):
        pass


    def search_relationships(self):
        pass


    def get_following(self):
        pass


    def get_followers(self):
        pass


    def export_network(self):
        pass
    
if __name__ == "__main__":
    neo = Neo4jAPI()
    # neo.add_bot({"id":0,"name":"Jonas","username":"Jonas_Pistolas"})
    # neo.add_user({"id":0,"name":"DS","username":"FenixD.S"})
    # neo.add_relationship({"id_1": 0, "id_2": 0, "type_1": "BOT", "type_2": "USER"})

    # print(neo.check_bot_exists(0))
    # print(neo.check_user_exists(0))

    neo.update_user({"id": 0, "name": "Diogo Ass"})
    neo.update_user({"id": 0, "username": "FenixDickSucker","name":"DS"})


    neo.close()
