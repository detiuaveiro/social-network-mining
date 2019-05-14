import psycopg2


class postgreSQL_API():
    
    def __init__(self, databaseName):
        try:
            # read connection parameters
            #params = config()

            # connect to the PostgreSQL server
            #print('Connecting to the PostgreSQL database...')
            self.databaseName=databaseName
            self.conn = psycopg2.connect(host="192.168.85.46", database=databaseName,user="postgres",password="password")

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
        self.cur = self.conn.cursor() 
        self.cur.execute("INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) VALUES (%s, %s, %s, %s, %s)", (timestamp, tweet_id, user_id, likes, retweets))
        self.conn.commit()
        self.cur.close()


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
            cur.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
    
    def getPoliciesByAPI(self,api):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies,api where api.id=policies.API_type and api.name=%s;",(api,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return list(result)
        except psycopg2.Error as e:
            cur.rollback()
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
            cur.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
    
    def getPoliciesByBot(self,bot_id):
        return list("TBD")
    
    def addPolicy(self,mapa):
        '''
        adiciona uma politica após confirmar que a api e o filter já estão na db
        '''
        try:
            #check if api exists
            cur=self.conn.cursor()
            cur.execute("select name from api where api.name=%s;",(mapa["API_type"],))
            data=cur.fetchone()
            if data is None:
                cur.execute("select count(id) from api;")
                count=cur.fetchone()
                val=count[0]+1
                cur.execute("insert into api (id,name) values (%s,%s);",(val,mapa["API_type"]))
            #check if filter exists
            cur.execute("select name from filter where filter.name=%s;",(mapa["filter"],))
            data=cur.fetchone()
            if data is None:
                cur.execute("select count(id) from filter;")
                count=cur.fetchone()
                val=count[0]+1
                cur.execute("insert into filter (id,name) values (%s,%s);",(val,mapa["filter"]))
            #check filter_api
            cur.execute("select api_id,filter_id from filter_api where api_id=%s and filter_id=%s;",(mapa["API_type"],mapa["filter"]))
            data=cur.fetchone()
            if data is None:
                cur.execute("insert into filter_api (api_id,filter_id) values (%s,%s);",(mapa["API_type"],mapa["filter"]))
            #add policy
            cur.execute("insert into policies (API_type,filter,name,params,active,id_policy) values (%s,%s,%s,%s,%s,%s);",(mapa["API_type"],mapa["filter"],mapa["name"],mapa["params"],mapa["active"],mapa["id_policy"]))
            self.conn.commit()
        except psycopg2.Error as e:
            cur.rollback()
            return [{"Error":e}]
        finally:
            cur.close()

        return [{"Message":"Success"}]
    
    def removePolicy(self,id):
        '''
        remove uma politica
        '''
        try:
            cur=self.conn.cursor()
            cur.execute("delete from policies where id_policy=%s;",(id,))
            self.conn.commit()
        except psycopg2.Error as e:
            cur.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
        return [{"Message":"Success"}]

    def updatePolicy(self,mapa):
        try:
            cur=self.conn.cursor()
            '''
            when updating, check api, filter and filter_api

            '''
            '''
            update query

            UPDATE table_name
            SET column1 = value1, column2 = value2...., columnN = valueN
            WHERE [condition];
            '''
            self.conn.commit()
        except psycopg2.Error as e:
            cur.rollback()
            return [{"Error":e}]
        finally:
            cur.close()
        return [{"Message":"Success"}]
    def postProcessResults(self,lista):
        d={}
        for i in lista:
            ll=[]
            for j in i:
                ll.append(j)
            d[i[0]]=ll
        return d