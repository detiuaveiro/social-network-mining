
import psycopg2


class postgreSQLConnect:
    
    def connect(self, databaseName):
        try:
            # read connection parameters
            #params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            conn = psycopg2.connect(host="192.168.85.46", database=databaseName,user="postgres",password="password")
            print(conn)
            return conn

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
	    
    def returnDataAndCloseConn(self, cur, conn):
	    data = cur.fetchone()
	    cur.close()
	    conn.close()
	    return data
	    
    def getDataTweets(self):
        conn = self.connect("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets")
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdTweet(self, tweet_id):
        conn = self.connect("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE tweet_id=%s", (tweet_id))
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdUser(self, user_id):
        conn = self.connect("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE user_id=%s", (user_id))
        return self.returnDataAndCloseConn(cur, conn)

    def getDataTweetsCompareTime(self, time1, time2, mode=0):
        conn = self.connect("postgres")
        cur = conn.cursor()
        cur.rollback()
        conn.close()
        #if mode==0:
            #cur.execute("SELECT * FROM tweets WHERE 

    def insertDataTweets(self, timestamp, tweet_id, user_id, likes, retweets):
        conn= self.connect("postgres")
        cur = conn.cursor() 
        cur.execute("INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) VALUES (%s, %s, %s, %s, %s)", (timestamp, tweet_id, user_id, likes, retweets))
        conn.commit()
        cur.close()


