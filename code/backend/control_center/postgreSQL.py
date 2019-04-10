
import psycopg2
from config import config


class postgreSQLConnect:
	
	def __init__(self):
		self.conn_dict = {"host":"localhost", "dbname":"", "user":"postgres", "password":""}
		
    def connect(self, conn_dict):
    """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()
 
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            conn = psycopg2.connect(conn_dict)
            return conn
 
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def selectDataConnection(self, database):
		self.conn_dict["dbname"] = database
		conn = self.connect(self.conn_dict)
		return conn
		
	def returnDataAndCloseConn(self, cur, conn):
		data = cur.fetchone()
		cur.close()
		conn.close()
		return data
    	
    def getDataTweets(self):
		conn = self.selectDataConnection("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets")
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdTweet(self, tweet_id):
        conn = self.selectDataConnection("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE tweet_id=%s", (tweet_id))
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdUser(self, user_id):
        conn = self.selectDataConnection("postgres")
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE user_id=%s", (user_id))
        return self.returnDataAndCloseConn(cur, conn)

    
    
    def getDataTweetsByTimestamp(self, timestamp):
        cur = self.conn.cursor() 
        cur.execute("INSERT INTO <name_table> VALUES <X, Y, Z>")
        conn.commit()
        cur.close()
