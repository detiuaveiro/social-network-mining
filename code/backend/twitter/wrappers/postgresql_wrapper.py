import psycopg2
import logging
import sys

sys.path.append("..")
import credentials

log = logging.getLogger("PostgreSQL")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class PostgresAnalysisAPI:
    """PostgreSQL

    Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
    Interacts with the snm_analysis_pg (for time series analysis) database
    """

    def __init__(self):
        log.debug("Connecting to PostgreSQL Analysis")
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(host=credentials.POSTGRES_URL, database=credentials.POSTGRES_ANALYSIS_DB,
                                         user=credentials.POSTGRES_USERNAME, password=credentials.POSTGRES_PASSWORD)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_tweet(self, data):
        """
        Attempts to insert a new Tweet item into the database

        @param data: The collection we want to insert the document into
        @return A success or failure message ({success: True/False ; error: None/Error})
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) values (DEFAULT,%s,%s,%s,%s);",
                (data["tweet_id"], data["user_id"], data["likes"], data["retweets"]))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as error:
            self.conn.rollback()

            log.error("ERROR INSERTING NEW TWEET")
            log.error(
                "Error: " + str(error)
            )
            return {"success": False, "error": error}

        return {"success": True}

    def insert_user(self, data):
        """
        Attempts to insert a new User item into the database

        @param data: The collection we want to insert the document into
        @return A success or failure message ({success: True/False ; error: None/Error})
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (timestamp, user_id, followers, following) values (DEFAULT,%s,%s,%s);",
                           (data["user_id"], data["followers"], data["following"]))
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as error:
            self.conn.rollback()

            log.error("ERROR INSERTING NEW USER")
            log.error(
                "Error: " + str(error)
            )
            return {"success": False, "error": error}

        return {"success": True}

    def search_tweet(self, data):
        pass

    def search_user(self, data):
        pass


class PostgresPoliciesAPI:
    """PostgreSQL

    Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
    Interacts with the snm_policies_pg (for bots' policies and PDP queries) database
    """

    def __init__(self):
        log.debug("Connecting to PostgreSQL Policies")
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(host=credentials.POSTGRES_URL, database=credentials.POSTGRES_POLICIES_DB,
                                         user=credentials.POSTGRES_USERNAME, password=credentials.POSTGRES_PASSWORD)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == "__main__":
    anal = PostgresAnalysisAPI()
    # anal.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 100, "retweets": 2})
    anal.insert_user({"user_id": 6253283, "followers": 10000, "following": 1234})
