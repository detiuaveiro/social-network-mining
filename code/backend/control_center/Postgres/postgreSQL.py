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

    ##################################################################################################################################
    '''
    These methods belong to the "postgres" database
    '''

    def addTweet(self,mapa):
        '''
        adiciona um tweet após confirmar que o tweet e o timestamp já está na db
        '''
        try:
            #check if tweet exists
            cur=self.conn.cursor()
            cur.execute("insert into tweets (timestamp, tweet_id, user_id, likes, retweets) values (DEFAULT,%s,%s,%s,%s);",(mapa["tweet_id"],mapa["user_id"],mapa["likes"],mapa["retweets"]))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()

        return [{"Message":"Success"}]

    def addUser(self,mapa):
        '''
        adiciona um tweet após confirmar que o tweet e o timestamp já está na db
        '''
        try:
            #check if user exists
            cur=self.conn.cursor()
            self.checkUserExistence(cur,mapa)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()

        return [{"Message":"Success"}]

    def getAllStatsTweets(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, tweet_id, likes, retweets from tweets;")
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getStatsTweetID(self, tweet_id):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, tweet_id, likes, retweets from tweets where tweet_id=%s;", (tweet_id,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getAllStatsUsers(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, user_id, followers, following from users;")
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getStatsUserID(self, user_id):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, user_id, followers, following from users where user_id=%s;", (user_id,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getAllStats(self):
        return self.getAllStatsTweets()+self.getAllStatsUsers()

    def checkUserExistence(self,cur, mapa):
        cur.execute("select * from users where user_id=%s;",(mapa["user_id"],))
        data=cur.fetchone()
        if data is None:
            #add user
            cur.execute("insert into users (timestamp, user_id, followers, following) values (DEFAULT,%s,%s,%s);",(mapa["user_id"],mapa["followers"],mapa["following"]))
        return

    ##################################################################################################################################
    '''
    These methods belong to the "policies" database
    '''
    
    def searchLog(self, id_bot):
        try:
            cur = self.conn.cursor()
            cur.execute("select * from logs where id_bot=%s;", (id_bot,))
            data = cur.fetchall()
            self.conn.commit()
            result = self.postProcessResults(data)

            for i in result.values():
                print(i[0])
                #bot_id=str(i["id_bot"])
                #i.pop("id_bot")
                #i["id_bot"]=bot_id

            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getAllLogs(self):
        try:
            cur = self.conn.cursor()
            cur.execute("select * from logs;")
            data = cur.fetchall()
            self.conn.commit()
            result = self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity: e.diag.message_primary}]
        finally:
            cur.close()

    def getAllPolicies(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies;")
            data=cur.fetchall()
            self.conn.commit()
            if len(data)==0:
                return []
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()
    
    def getPoliciesByAPI(self,api):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies,api where api.id=policies.API_type and api.name=%s;",(api,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()

    def getPoliciesByID(self,id):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies where policies.id_policy=%s;",(id,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            return [result]
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()
    
    def getPoliciesByBot(self,bot_id):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies;")
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data)
            '''
            {id_policy:[api,filter,params,etc]}
            '''
            lista=[]
            for i in result:
                for j in result[i]:
                    if type(j) is list:
                        response=self.searchForBot(j,bot_id)
                        if response:
                            lista.append(result[i])        
            return lista
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()

    def addLog(self,mapa):
        '''
        adiciona uma politica após confirmar que a api e o filter já estão na db
        '''
        try:
            #add log
            cur=self.conn.cursor()
            cur.execute("insert into logs (id_bot,timestamp,action) values (%s,DEFAULT,%s);",(mapa["id_bot"], mapa["action"]))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()

        return [{"Message":"Success"}]

    def addPolicy(self,mapa):
        '''
        adiciona uma politica após confirmar que a api e o filter já estão na db
        '''
        try:
            #check if api exists
            cur=self.conn.cursor()
            self.checkAPIExistence(cur,mapa)
            #check if filter exists
            self.checkFilterExistence(cur,mapa)
            #check filter_api
            self.checkFilterAPIExistence(cur,mapa)
            #add policy
            cur.execute("insert into policies (API_type,filter,name,params,active,id_policy) values (%s,%s,%s,%s,%s,%s);",(mapa["API_type"],mapa["filter"],mapa["name"],mapa["params"],mapa["active"],mapa["id_policy"]))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
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
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()
        return [{"Message":"Success"}]

    def updatePolicy(self,mapa):
        '''
        This function only updates records with the specified fields received.
        mapa is a dictionary with the information needed to update the record (fields to be updated + id_policy)
        '''
        flag=0
        try:
            cur=self.conn.cursor()
            '''
            when updating, check api, filter and filter_api
            '''
            if "API_type" in list(mapa.keys()):
                self.checkAPIExistence(cur,mapa)
                flag=1

            if "filter" in list(mapa.keys()):
                self.checkFilterExistence(cur,mapa)
                flag=1
            
            if flag==1:
                self.checkFilterAPIExistence(cur,mapa)
            
            #update query
            for i in mapa:
                if i=="id_policy":
                    pass
                else:
                    cur.execute("update policies set %s=%s where policies.id=%s",(i,mapa[i],mapa["id_policy"]))

            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            return [{e.diag.severity : e.diag.message_primary}]
        finally:
            cur.close()
        return [{"Message":"Success"}]

    def postProcessResults(self,lista):
        d={}
        for i in lista:
            ll=[]
            for j in i:
                ll.append(j)
            d[i[-1]]=ll
        return d

    def checkAPIExistence(self,cur,mapa):
        cur.execute("select name from api where api.name=%s;",(mapa["API_type"],))
        data=cur.fetchone()
        if data is None:
            cur.execute("select count(id) from api;")
            count=cur.fetchone()
            val=count[0]+1
            cur.execute("insert into api (id,name) values (%s,%s);",(val,mapa["API_type"]))
        return
            
    
    def checkFilterExistence(self,cur,mapa):
        cur.execute("select name from filter where filter.name=%s;",(mapa["filter"],))
        data=cur.fetchone()
        if data is None:
            cur.execute("select count(id) from filter;")
            count=cur.fetchone()
            val=count[0]+1
            cur.execute("insert into filter (id,name) values (%s,%s);",(val,mapa["filter"]))            
        return

    def checkFilterAPIExistence(self,cur,mapa):
        cur.execute("select id from api where api.name=%s",(mapa["API_type"],))
        id_api=cur.fetchone()
        cur.execute("select id from filter where filter.name=%s",(mapa["filter"],))
        id_filter=cur.fetchone()
        cur.execute("select api_id,filter_id from filter_api where api_id=%s and filter_id=%s;",(id_api,id_filter))
        data=cur.fetchone()
        if data is None:
            cur.execute("insert into filter_api (api_id,filter_id) values (%s,%s);",(id_api,id_filter))
        return

    def searchForBot(self,lista,id_bot):
        '''
        lista is the parameter list. now, search for the bot!
        '''
        for i in lista:
            if i==id_bot:
                return True
        return False