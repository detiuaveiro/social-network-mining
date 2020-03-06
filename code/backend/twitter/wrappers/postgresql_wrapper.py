import psycopg2
import logging
import sys

sys.path.append("..")
import credentials
import datetime

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

    def search_tweet(self, params=None):
        """
        Searches and returns all Tweets if no data is specified, or the specific tweet matching the given parameters

        @param params: The parameters we want to query
        @return The query's result or error
        """

        try:
            cursor = self.conn.cursor()

            query = "select timestamp, tweet_id, likes, retweets from tweets "
            if params == None:
                query += ";"
            else:
                query += "WHERE "
                control = 0
                if "tweet_id" in params.keys():
                    query += "tweet_id = " + params["tweet_id"]
                    control = 1
                if "likes" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "likes = " + params["likes"]
                    control = 1
                if "retweets" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "retweets = " + params["retweets"]

                query += ";"

            cursor.execute(query)

            data = cursor.fetchall()

            self.conn.commit()
            cursor.close()

            # result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
            result = []  # Array of jsons
            for tuple in data:
                result.append({"timestamp": tuple[0], "tweet_id": tuple[1], "likes": tuple[2], "retweets": tuple[3]})

            return {"success": True, "data": result}
        except psycopg2.Error as e:
            self.conn.rollback()
            return {"success": False, "error": error}

    def search_user(self, params=None):
        """
        Searches and returns all Users if no data is specified, or the specific tweet matching the given parameters

        @param params: The parameters we want to query
        @return The query's result or error
        """

        try:
            cursor = self.conn.cursor()

            query = "select timestamp, user_id, followers, following from users "
            if params == None:
                query += ";"
            else:
                query += "WHERE "
                control = 0
                if "user_id" in params.keys():
                    query += "user_id = " + params["user_id"]
                    control = 1
                if "user_id" in params.keys():
                    query += "user_id = " + params["user_id"]
                    control = 1
                if "followers" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "followers = " + params["followers"]
                    control = 1
                if "following" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "following = " + params["following"]

                query += ";"

            cursor.execute(query)

            data = cursor.fetchall()

            self.conn.commit()
            cursor.close()

            # result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
            result = []  # Array of jsons
            for tuple in data:
                result.append(
                    {"timestamp": tuple[0], "user_id": tuple[1], "followers": tuple[2], "following": tuple[3]})

            return {"success": True, "data": result}
        except psycopg2.Error as e:
            self.conn.rollback()
            return {"success": False, "error": error}


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


    def search_tweet(self, params=None):
        """
        Searches and returns all Tweets if no data is specified, or the specific tweet matching the given parameters

        @param params: The parameters we want to query
        @return The query's result or error
        """

        try:
            cursor = self.conn.cursor()

            query = "select timestamp, tweet_id, likes, retweets from tweets "
            if params == None:
                query += ";"
            else:
                query += "WHERE "
                control = 0
                if "tweet_id" in params.keys():
                    query += "tweet_id = " + params["tweet_id"]
                    control = 1
                if "likes" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "likes = " + params["likes"]
                    control = 1
                if "retweets" in params.keys():
                    if control == 1:
                        query += " AND "
                    query += "retweets = " + params["retweets"]

                query += ";"

            cursor.execute(query)

            data = cursor.fetchall()

            self.conn.commit()
            cursor.close()

            # result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
            result = []  # Array of jsons
            for tuple in data:
                result.append({"timestamp": tuple[0], "tweet_id": tuple[1], "likes": tuple[2], "retweets": tuple[3]})

            return {"success": True, "data": result}
        except psycopg2.Error as e:
            self.conn.rollback()
            return {"success": False, "error": error}


if __name__ == "__main__":
    # TODO: Test and implement searching by timestamp ; Policies API
    anal = PostgresAnalysisAPI()
    # anal.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 100, "retweets": 2})
    # anal.insert_user({"user_id": 6253283, "followers": 10000, "following": 1234})
    for i in anal.search_tweet()["data"]:
        print(i)
    for i in anal.search_user()["data"]:
        print(i)

    # print(datetime.datetime.now())
