import datetime
import credentials
import psycopg2
import logging
import sys

sys.path.append("..")

log = logging.getLogger("PostgreSQL")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class PostgresAPI:
    """PostgreSQL

    Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
    """

    def __init__(self):
        log.debug("Connecting to PostgreSQL Analysis")
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(host=credentials.POSTGRES_URL, database=credentials.POSTGRES_DB,
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
                result.append(
                    {"timestamp": tuple[0], "tweet_id": tuple[1], "likes": tuple[2], "retweets": tuple[3]})

            return {"success": True, "data": result}
        except psycopg2.Error as error:
            self.conn.rollback()
            return {"success": False, "error": error}

    def search_user(self, params=None):
        """sudo -u postgres psql

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
        except psycopg2.Error as error:
            self.conn.rollback()
            return {"success": False, "error": error}

    def search_logs(self, params=None, limit=None):
        """
        Searches and returns all logs if no data is specified, or the specific logs matching the parameters. Can also specify the amount of logs to be retrieved.
        Data retrieved is ordered by the most recent

        @param params: The parameters we want to query. Right now only bot_id is supported
        @param limit: An optional parameter specifying the amount of logs to be retrieved

        @return The query's result or error
        """

        try:
            cursor = self.conn.cursor()

            query = f"select * from logs " \
                    f"{'WHERE' if params is not None else ''} " \
                    f"{'id_bot=' + params['bot_id'] if params is not None and 'bot_id' in params.keys() else ''} " \
                    f"ORDER BY timestamp DESC " \
                    f"{'limit ' + str(limit) if limit is not None else ''} ;"


            cursor.execute(query)
            print(query)


            data = cursor.fetchall()

            self.conn.commit()
            cursor.close()

            # result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
            result = []  # Array of jsons

            for tuple in data:
                result.append(
                    {"id_bot": tuple[0], "timestamp": tuple[1], "action": tuple[2]})

            return {"success": True, "data": result}
        except psycopg2.Error as error:
            self.conn.rollback()
            return {"success": False, "error": error}

    def search_policies(self, params=None, limit=None):
        """
        Searches and returns all policies if no data is specified, or the specific policies matching the parameters. Can also specify the amount of poliecies to be retrieved.

        @param params: The parameters we want to query. Right now only bot_id is supported
        @param limit: An optional parameter specifying the amount of logs to be retrieved

        @return The query's result or error
        """

        try:
            cursor = self.conn.cursor()

            query = f"select api.name,policies.name,params,active,id_policy,filter.name from policies " \
                    f"   left outer join filter on filter.id=policies.filter " \
                    f"   left outer join api on api.id=policies.API_type " \
                    f"{'WHERE' if params is not None else ''} " \
                    f"{'api.name=' + params['api_name'] if params is not None and 'api_name' in params.keys() else ''} " \ 
                    f"{'policies.id_policy=' + params['policy_id'] if params is not None and 'policy_id' in params.keys() else ''} " \
                    f"{'policies.id_policy=' + params['policy_id'] if params is not None and 'policy_id' in params.keys() else ''} " \

            cursor.execute(query)

            data = cursor.fetchall()

            self.conn.commit()
            cursor.close()

            result = []  # Array of jsons
            for tuple in data:
                result.append(
                    {"API_type": tuple[0], "name": tuple[1], "bots": [], "params": [], "active": tuple[3],
                     "policy_id": tuple[4], "filter": tuple[5]})
                min_bot_len = 19
                for param in tuple[2]:
                    if param.isnumeric() and len(param) >= min_bot_len:
                        result["bots"].append(param)
                    else:
                        result["params"].append(param)

            return {"success": True, "data": result}
        except psycopg2.Error as error:
            self.conn.rollback()
            return {"success": False, "error": error}


if __name__ == "__main__":
    # TODO: Test and implement searching by timestamp ; Policies API
    anal = PostgresAPI()
    # anal.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 100, "retweets": 2})
    # anal.insert_user({"user_id": 6253283, "followers": 10000, "following": 1234})
    # try:
    #    for i in anal.search_tweet()["data"]:
    #        print(i)
    # except:
    #    print(anal.search_tweet()["error"])

    # try:
    #    for i in anal.search_user()["data"]:
    #        print(i)
    # except:
    #    print(anal.search_tweet()["error"])

    result = anal.search_logs(limit=10)
    if result["success"]:
        for i in result["data"]:
            print(i)
    else:
        print(anal.search_tweet()["error"])
