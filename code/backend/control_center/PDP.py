import json
import psycopg2
import redis

class PDP:
    '''
    Open connection with databases:
        - Policy database (postgresql)
        - Logging database (redis)
    Check params for psycopg2 (port 5432 is default of postgres)
    Check host, port and password for redis
    '''
    def __init__(self):
        self.conn=psycopg2.connect(dbname="NOME_DA_DB", user="NOME_DO_USER", password="PASSWORD", host="HOSTNAME", port=5432)
        self.log=redis.Redis(host='HOSTNAME',port=8443,password='PASSWORD')
        return
    
    def receive_request(self,msg):
        #json loads do PEP
        message=json.loads(msg)
        return self.evaluate(message)
        
    '''
    workflow of this function
        - pre-processing of request (filter, prepare db request, etc)
        - request to DB
        - get request from DB
        - post-processing of response (clean response from db, etc)
        - DECIDE (PERMIT, DENY)
    
    msg- dictionary with necessary fields to perform the query
    '''
    def evaluate(self,msg):
        
        evaluate_answer=True

        #PRE-PROCESSING the request to get the QUERY
        query=""

        cur=self.conn.cursor()
        try:
            cur.execute(query) #execute("QUERY")
            DB_val=cur.fetchall() #or fetchone()

            #check DB_val, post-process result

            self.conn.commit()
            #log to the Redis the action is successful
            #BOT X performed query Y
        except psycopg2.Error as e:
            #log to the Redis the action failed
            #BOT X performed query Y with following error: e.pgcode , e.pgerror
            self.conn.rollback()
            evaluate_answer=False
        finally:
            cur.close()

        if evaluate_answer:
            return self.send_response({"response":"PERMIT"})
        else:
            return self.send_response({"response":"DENY"})
        
    def send_response(self,msg):
        #json dumps da decisão
        message=json.dumps(msg)
        return message #pep.receive_response(message)
        