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
            for i in result:
                i['tweet_id']=str(i['tweet_id'])
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
            for i in result:
                i['tweet_id']=str(i['tweet_id'])
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
            for i in result:
                i['user_id']=str(i['user_id'])
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
            for i in result:
                i['user_id']=str(i['user_id'])
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
            print(data[0])
            result=self.getClearLogs(data,["id","timestamp","action"])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getAllLogs(self):
        try:
            cur = self.conn.cursor()
            cur.execute("select * from logs order by timestamp DESC;")
            data = cur.fetchall()
            self.conn.commit()

            result = self.getClearLogs(data,["id","timestamp","action"])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity: e.diag.message_primary}

    def getAllPolicies(self):
        try:
            cur=self.conn.cursor()
            cur.execute("select api.name,policies.name,params,active,id_policy,filter.name from policies left outer join filter on filter.id=policies.filter left outer join api on api.id=policies.API_type;")
            data=cur.fetchall()
            self.conn.commit()
            if len(data)==0:
                return []
            result=self.postProcessResults(data,['API_type','name','params','active','id_policy','filter'])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
    
    def getPoliciesByAPI(self,api):
        try:
            cur=self.conn.cursor()
            cur.execute("select api.name,filter.name,policies.name,policies.params,policies.active,policies.id_policy from policies left outer join filter on filter.id=policies.filter left outer join api on api.id=policies.API_type where api.name=%s;",(api,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data,
            ['API_type','filter','name','params','active','id_policy'])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}

    def getPoliciesByID(self,id):
        try:
            cur=self.conn.cursor()
            cur.execute("select api.name,policies.name,params,active,id_policy,filter.name from policies left outer join filter on filter.id=policies.filter left outer join api on api.id=policies.API_type where policies.id_policy=%s;",(id,))
            data=cur.fetchall()
            self.conn.commit()
            result=self.postProcessResults(data,['API_type','name','params','active','id_policy','filter'])
            cur.close()
            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            return {e.diag.severity : e.diag.message_primary}
    
    def getPoliciesByBot(self,bot_id):
        bot_id=str(bot_id)
        try:
            cur=self.conn.cursor()
            cur.execute("select api.name,policies.name,params,active,id_policy,filter.name from policies left outer join filter on filter.id=policies.filter left outer join api on api.id=policies.API_type;")
            data=cur.fetchall()
            self.conn.commit()
            cur.close()
            result=self.postProcessResults(data,['API_type','name','params','active','id_policy','filter'])
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
            self.checkFilterAPIExistence(cur,mapa,api,filtro)
            #add policy
            if "bots" in mapa.keys():
                if len(mapa["bots"])==0:
                    return {"ERROR":"No bots associated"}
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
        try:
            cur=self.conn.cursor()
            '''
            when updating, check api, filter and filter_api
            '''
            if "API_type" in mapa.keys():
                api=self.checkAPIExistence(cur,mapa)
            if "filter" in mapa.keys():
                filtro=self.checkFilterExistence(cur,mapa)
            
            if "bots" in mapa.keys():
                if len(mapa["bots"])==0:
                    return {"ERROR":"No bots associated"}
                if "filter" in mapa.keys() and mapa["filter"]=="Keywords" and "params" in mapa.keys():
                    if len(mapa["bots"])==1:
                        mapa["params"].insert(0,str(mapa["bots"][0]))
                    elif len(mapa["bots"])>1:
                        for i in mapa["bots"]:
                            mapa["params"].insert(0,str(i))
                elif "filter" in mapa.keys() and mapa["filter"]=="Target" and "params" in mapa.keys():
                    if len(mapa["bots"])==1:
                        mapa["params"].append(str(mapa["bots"][0]))
                    elif len(mapa["bots"])>1:
                        for j in mapa["bots"]:
                            mapa["params"].append(str(j))
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
        '''
        This function gets the result from the postgres and post-process it to the JSON standard
        const MINIMUM_LENGTH_BOT_ID avoids that numeric keywords such as 911 or 112 to be confused as a bot
        '''
        l=[]
        MINIMUM_LENGTH_BOT_ID=19
        for i in lista:
            d={}
            num=0
            bots_list=[]
            params=[]
            if "Keywords" in i and "filter" in cols:
                for j in i:
                    if len(i)==num:
                        pass
                    else:
                        if cols[num]=="params":
                            bots_list.append(j[0])
                            for k in j[1:]:
                                if k.isnumeric() and len(k)>=MINIMUM_LENGTH_BOT_ID:
                                    bots_list.append(k)
                                else:
                                    params.append(k)
                            d["bots"]=bots_list
                            d[cols[num]]=params
                        else:
                            d[cols[num]]=j
                        num+=1
            elif "Target" in i and "filter" in cols:
                for j in i:
                    if len(i)==num:
                        pass
                    else:
                        if cols[num]=="params":
                            params.append(j[0])
                            for k in j[1:]:
                                bots_list.append(k)
            else:
                for j in i:
                    if len(i)==num:
                        pass
                    else:
                        d[cols[num]]=j
                        num+=1
            l.append(d)
        return l

    def checkAPIExistence(self,cur,mapa):
        cur.execute("select * from api where api.name=%s;",(mapa["API_type"],))
        data=cur.fetchone()
        cur.execute("select count(id) from api;")
        count=cur.fetchone()
        if data is None:
            val=count[0]+1
            cur.execute("insert into api (id,name) values (%s,%s);",(val,mapa["API_type"]))
            return val
        return data[0]
            
    
    def checkFilterExistence(self,cur,mapa):
        cur.execute("select * from filter where filter.name=%s;",(mapa["filter"],))
        data=cur.fetchone()
        cur.execute("select count(id) from filter;")
        count=cur.fetchone()
        if data is None:
            val=count[0]+1
            cur.execute("insert into filter (id,name) values (%s,%s);",(val,mapa["filter"]))
            return val           
        return data[0]

    def checkFilterAPIExistence(self,cur,mapa,id_api,id_filter):
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
        result = self.postProcessResults(data,cols)
        for j in result:
            j["id"]=str(j["id"])
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
    