
import psycopg2


class postgreSQLConnect:
    
    def connect(self, databaseName):
        try:
            # read connection parameters
            #params = config()

            # connect to the PostgreSQL server
            #print('Connecting to the PostgreSQL database...')
            self.databaseName=databaseName
            self.conn = psycopg2.connect(host="192.168.85.46", database=databaseName,user="postgres",password="password")
            return self.conn

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
	    
    def returnDataAndCloseConn(self, cur, conn):
	    data = cur.fetchone()
	    cur.close()
	    conn.close()
	    return data

    def getDataTweets(self):
        conn = self.connect(self.databaseName)
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets")
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdTweet(self, tweet_id):
        conn = self.connect(self.databaseName)
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE tweet_id=%s", (tweet_id))
        return self.returnDataAndCloseConn(cur, conn)
        
    def getDataTweetsByIdUser(self, user_id):
        conn = self.connect(self.databaseName)
        cur = conn.cursor() 
        cur.execute("SELECT * FROM tweets WHERE user_id=%s", (user_id))
        return self.returnDataAndCloseConn(cur, conn)

    def getDataTweetsCompareTime(self, time1, time2, mode=0):
        conn = self.connect(self.databaseName)
        cur = conn.cursor()
        cur.rollback()
        conn.close()
        #if mode==0:
            #cur.execute("SELECT * FROM tweets WHERE 

    def insertDataTweets(self, timestamp, tweet_id, user_id, likes, retweets):
        conn= self.connect(self.databaseName)
        cur = conn.cursor() 
        cur.execute("INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) VALUES (%s, %s, %s, %s, %s)", (timestamp, tweet_id, user_id, likes, retweets))
        conn.commit()
        cur.close()

##################################################################################################################################
    '''
    These methods belong to the "policies" database
    '''
    def getAllPolicies(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies;")
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return list(result)
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
    
    def getPoliciesByAPI(self,api):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies,api where api.id=policies.API_type and api.name=%s;",(api))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return list(result)
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{"Error":e}]
        finally:
            cur.close()

    def getPoliciesByID(self,id):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies where policies.id_policy=%s;",(id,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return list(result)
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
    
    def getPoliciesByBot(self,bot_id):
        return list("TBD")
    
    def addPolicy(self,lista):
        
        return list("hehe")
    
    def removePolicy(self,id):
        try:
            cur=self.conn.cursor()
            cur.execute("delete from policies where id_policy=%s;",(id,))
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
        return list("hehe")

    def postProcessResults(self,lista):
        d={}
        for i in lista:
            ll=[]
            for j in i:
                ll.append(j)
            d[i[0]]=ll
        return d
