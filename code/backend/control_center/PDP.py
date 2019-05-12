import json
import psycopg2

class PDP:
    '''
    Open connection with databases:
        - Policy database (postgresql)
    Port 5432 is default of postgres
    '''
    def __init__(self):
        self.conn=psycopg2.connect(host="192.168.85.46",database="policies", user="postgres", password="password")
        return
    
    def receive_request(self,msg):
        #json loads do PEP
        message=json.loads(msg)
        return self.evaluate(message)
        
    def evaluate(self,msg):
        '''
        workflow of this function
        - pre-processing of request (filter, prepare db request, etc)
        - request to DB
        - get request from DB
        - post-processing of response (clean response from db, etc)
        - DECIDE (PERMIT, DENY)
    
        msg- dictionary with necessary fields to perform the query
        msg={"name":action}
        '''
        evaluate_answer=True

        #PRE-PROCESSING the request to get the QUERY
        '''
        prepare the query according to the request
        for now, all the REQUEST_TWEET* will be admitted.
        in a recent future, it will evolve into two types:
            - based on a heuristic (if it's in the threshold, request accepted): 0 to 1
            - based on a target (user)
        '''
        if msg["request"]=="REQUEST_TWEET_LIKE" or msg["request"]==5:
            '''
            bot_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["request"]=="REQUEST_TWEET_RETWEET" or msg["request"]==6:
            '''
            bot_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["request"]=="REQUEST_TWEET_REPLY" or msg["request"]==7:
            '''
            bot_id        
            tweet_id
            tweet_text
            tweet_entities
            tweet_in_reply_to_status_id_str
            tweet_in_reply_to_user_id_str
            tweet_in_reply_to_screen_name
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["request"]=="REQUEST_FOLLOW_USER" or msg["request"]==8:
            '''
            bot_id
            tweet_user_id
            '''
            query=""
        else:
            return self.send_response({"response":"DENY"})

        cur=self.conn.cursor()
        try:
            cur.execute(query)
            DB_val=cur.fetchall() #or fetchone()
            #needs revision
            num=len(DB_val)
            self.conn.commit()
            
            #check DB_val, post-process result
            data=self.postProcess(num,DB_val)
            
            #apply the heuristics here

        except psycopg2.Error:
            self.conn.rollback()
            evaluate_answer=False
        finally:
            cur.close()
            self.conn.close()

        if evaluate_answer:
            return self.send_response({"response":"PERMIT"})
        else:
            return self.send_response({"response":"DENY"})
        
    def postProcess(self,num,DB_val):
        if num==1:
            d={}
            ll=[]
            for i in DB_val:
                ll.append(i)
            d[i[0]]=ll
            return d
        elif num>1:
            d={}
            for i in DB_val:
                ll=[]
                for j in i:
                    ll.append(j)
                d[i[0]]=ll            
            return d
        else:
            return self.send_response({"response":"DENY"})
            
    def send_response(self,msg):
        #json dumps da decisão
        message=json.dumps(msg)
        return message #pep.receive_response(message)
        