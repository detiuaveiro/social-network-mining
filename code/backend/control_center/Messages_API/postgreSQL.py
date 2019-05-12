import psycopg2


class postgreSQL_API:
    
    def __init__(self, databaseName):
        try:
            # read connection parameters
            #params = config()

            # connect to the PostgreSQL server

            print("Connecting to PostgresSQL")

            self.conn = psycopg2.connect(host="192.168.85.46", database=databaseName,user="postgres",password="password")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insertDataTweets(self, timestamp, tweet_id, user_id, likes, retweets):
        self.cur = self.conn.cursor() 
        self.cur.execute("INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) VALUES (%s, %s, %s, %s, %s)", (timestamp, tweet_id, user_id, likes, retweets))
        self.conn.commit()
        self.cur.close()

