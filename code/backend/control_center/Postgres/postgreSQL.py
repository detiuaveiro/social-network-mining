import psycopg2
from datetime import datetime


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
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)
            return {e.diag.severity : e.diag.message_primary}
        
        return {"Message":"Success"}

    def addUser(self,mapa):
        '''
        adiciona um tweet após confirmar que o tweet e o timestamp já está na db
        '''
        try:
            #check if user exists
            cur=self.conn.cursor()
            self.checkUserExistence(cur,mapa)
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
        
        return {"Message":"Success"}

    def getAllStatsTweets(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, tweet_id, likes, retweets from tweets;")
            data=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['timestamp','tweet_id','likes','retweets'])
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getStatsTweetID(self, tweet_id):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, tweet_id, likes, retweets from tweets where tweet_id=%s;", (tweet_id,))
            data=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['timestamp', 'tweet_id', 'likes', 'retweets'])
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getAllStatsUsers(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, user_id, followers, following from users;")
            data=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['timestamp', 'user_id', 'followers', 'following'])
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getStatsUserID(self, user_id):
        try:
            cur=self.conn.cursor()
            cur.execute("select timestamp, user_id, followers, following from users where user_id=%s;", (user_id,))
            data=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['timestamp', 'user_id', 'followers', 'following'])
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

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
            cur.execute("select * from logs where id_bot=%s order by timestamp DESC;", (id_bot,))
            data = cur.fetchall()
            self.conn.commit()

            result=self.getClearLogs(data,["id","timestamp","action","converted"])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getAllLogs(self):
        try:
            cur = self.conn.cursor()
            cur.execute("select * from logs;")
            data = cur.fetchall()
            self.conn.commit()

            result = self.getClearLogs(data,["id","timestamp","action","converted"])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getAllPolicies(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies;")
            data=cur.fetchall()
            cur.execute("select * from filter")
            filters=cur.fetchall()
            cur.execute("select * from api")
            apis=cur.fetchall()            
            self.conn.commit()
            if len(data)==0:
                return []
            result=self.postProcessResults(data,['API_type','filter','name','params','active','id_policy'])
            cur.close()
            for i in result:
                for j in filters:
                    if j[0]==i['filter']:
                        i['filter']=j[1]
                for k in apis:
                    if k[0]==i['API_type']:
                        i['API_type']=k[1]
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
    
    def getPoliciesByAPI(self,api):
        try:
            cur=self.conn.cursor()
            cur.execute("select policies.API_type,policies.filter,policies.name,policies.params,policies.active,policies.id_policy,api.name from policies,api where api.id=policies.API_type and api.name=%s;",(api,))
            data=cur.fetchall()
            cur.execute("select * from filter")
            filters=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data,
            ['API_type','filter','name','params','active','id_policy','API_name'])
            cur.close()
            for i in result:
                del i['API_type']
                for j in filters:
                    if j[0]==i['filter']:
                        i['filter']=j[1] 
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}

    def getPoliciesByID(self,id):
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies where policies.id_policy=%s;",(id,))
            data=cur.fetchall()
            cur.execute("select * from filter")
            filters=cur.fetchall()
            cur.execute("select * from api")
            apis=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data,['API_type','filter','name','params','active','id_policy'])
            cur.close()
            for i in result:
                for j in filters:
                    if j[0]==i['filter']:
                        i['filter']=j[1]
                for k in apis:
                    if k[0]==i['API_type']:
                        i['API_type']=k[1]
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
    
    def getPoliciesByBot(self,bot_id):
        bot_id=str(bot_id)
        try:
            cur=self.conn.cursor()
            cur.execute("select * from policies;")
            data=cur.fetchall()
            cur.execute("select * from filter")
            filters=cur.fetchall()
            cur.execute("select * from api")
            apis=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['API_type','filter','name','params','active','id_policy'])
            '''
            {id_policy:[api,filter,params,etc]}
            '''
            lista=[]
            for i in result:
                for j in i.keys():
                    if j=="params":
                        response=self.searchForBot(i[j],bot_id)
                        if response:
                            lista.append(i)
            
            for j in lista:
                for k in filters:
                    if k[0]==j['filter']:
                        j['filter']=k[1]
                for l in apis:
                    if l[0]==j['API_type']:
                        j['API_type']=l[1]
            return lista
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}

    def addLog(self,mapa):
        '''
        adiciona uma politica após confirmar que a api e o filter já estão na db
        '''
        try:
            #add log
            cur=self.conn.cursor()
            cur.execute("insert into logs (id_bot,timestamp,action) values (%s,DEFAULT,%s);",(mapa["id_bot"], mapa["action"]))
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}

        return {"Message":"Success"}

    def addPolicy(self,mapa):
        '''
        adiciona uma politica após confirmar que a api e o filter já estão na db
        '''
        try:
            #check if api exists
            cur=self.conn.cursor()
            api=self.checkAPIExistence(cur,mapa)
            #check if filter exists
            filtro=self.checkFilterExistence(cur,mapa)
            #check filter_api
            self.checkFilterAPIExistence(cur,mapa)
            #add policy
            if mapa["filter"]=="Keywords":
                if len(mapa["bots"])==1:
                    mapa["params"].insert(0,str(mapa["bots"][0]))
                elif len(mapa["bots"])>1:
                    for i in mapa["bots"]:
                        mapa["params"].insert(0,str(i))
            elif mapa["filter"]=="Target":
                if len(mapa["bots"])==1:
                    mapa["params"].append(str(mapa["bots"][0]))
                elif len(mapa["bots"])>1:
                    for j in mapa["bots"]:
                        mapa["params"].append(str(j))
            if "active" in mapa.keys():
                print(cur.mogrify("insert into policies (API_type,filter,name,params,active) values (%s,%s,%s,%s,%s);",(api,filtro,mapa["name"],mapa["params"],mapa["active"])))
                cur.execute("insert into policies (API_type,filter,name,params,active) values (%s,%s,%s,%s,%s);",(api,filtro,mapa["name"],mapa["params"],mapa["active"]))
            else:
                cur.execute("insert into policies (API_type,filter,name,params) values (%s,%s,%s,%s);",(api,filtro,mapa["name"],mapa["params"]))
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}

        return {"Message":"Success"}
    
    def removePolicy(self,id):
        '''
        remove uma politica
        '''
        try:
            cur=self.conn.cursor()
            cur.execute("delete from policies where id_policy=%s;",(id,))
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
        return {"Message":"Success"}

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
            if "API_type" in mapa.keys():
                api=self.checkAPIExistence(cur,mapa)
                flag+=0.5
            if "filter" in mapa.keys():
                filtro=self.checkFilterExistence(cur,mapa)
                flag+=1

            if flag==1.5:
                self.checkFilterAPIExistence(cur,mapa)
            elif flag==1:
                self.checkFilterAPIExistence(cur,mapa,ap=False)
            elif flag==0.5:
                self.checkFilterAPIExistence(cur,mapa,fil=False)
            #update query
            for i in mapa:
                if i=="API_type":
                    cur.execute("update policies set API_type=%s where policies.id_policy=%s",(api,mapa["id_policy"]))
                elif i=="filter":
                    cur.execute("update policies set filter=%s where policies.id_policy=%s",(filtro,mapa["id_policy"]))
                elif i=="name":
                    cur.execute("update policies set name=%s where policies.id_policy=%s",(mapa[i],mapa["id_policy"]))
                elif i=="params":
                    cur.execute("update policies set params=%s where policies.id_policy=%s",(mapa[i],mapa["id_policy"]))
                elif i=="active":
                    cur.execute("update policies set active=%s where policies.id_policy=%s",(mapa[i],mapa["id_policy"]))
                else:
                    pass    
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
        return {"Message":"Success"}

    def postProcessResults(self,lista,cols):
        l=[]
        for i in lista:
            d={}
            num=0
            for j in i:
                if len(i)==num:
                    pass
                else:
                    d[cols[num]]=j
                    num+=1
            l.append(d)
        return l

    def checkAPIExistence(self,cur,mapa):
        cur.execute("select name from api where api.name=%s;",(mapa["API_type"],))
        data=cur.fetchone()
        cur.execute("select count(id) from api;")
        count=cur.fetchone()
        if data is None:
            val=count[0]+1
            cur.execute("insert into api (id,name) values (%s,%s);",(val,mapa["API_type"]))
            return val
        return count[0]
            
    
    def checkFilterExistence(self,cur,mapa):
        cur.execute("select name from filter where filter.name=%s;",(mapa["filter"],))
        data=cur.fetchone()
        cur.execute("select count(id) from filter;")
        count=cur.fetchone()
        if data is None:
            val=count[0]+1
            cur.execute("insert into filter (id,name) values (%s,%s);",(val,mapa["filter"]))
            return val           
        return count[0]

    def checkFilterAPIExistence(self,cur,mapa,ap=True,fil=True):
        if ap:
            cur.execute("select id from api where api.name=%s",(mapa["API_type"],))
            id_api=cur.fetchone()
        if fil:
            cur.execute("select id from filter where filter.name=%s",(mapa["filter"],))
            id_filter=cur.fetchone()
        if ap and fil:
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

    def getClearLogs(self,data,cols):
        lista=[]
        for i in data:
            a=i+(datetime.timestamp(i[1]),)
            lista.append(a)
        result = self.postProcessResults(lista,cols)
        for j in result:
            bot_id=str(j["id"])
            del j["id"]
            if "converted" in j.keys():
                del j["converted"]
            j["id"]=bot_id
        return result
    
    def getPoliciesParams(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select params from policies,filter where policies.active=TRUE and policies.filter=filter.id and filter.name='Target'")
            DB_val=cur.fetchall()
            self.conn.commit()
            cur.close()
            return DB_val
        except psycopg2.Error as e:
            self.conn.rollback()
            return e.diag.severity
    