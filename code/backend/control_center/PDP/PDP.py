import json
import psycopg2
from enum import IntEnum

class PoliciesTypes(IntEnum):
    REQUEST_TWEET_LIKE = 1
    REQUEST_TWEET_RETWEET = 2
    REQUEST_TWEET_REPLY = 3
    REQUEST_FOLLOW_USER = 4
    FIRST_TIME = 5

class PDP:
    '''
    Open connection with databases:
        - Policy database (postgresql)
    Port 5432 is default of postgres
    '''
    def __init__(self):
        self.conn=psycopg2.connect(host="192.168.85.46",database="policies", user="postgres", password="password")
        self.PoliciesTypes=PoliciesTypes(4)
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
        if msg["type"]==PoliciesTypes.REQUEST_TWEET_LIKE:
            '''
            bot_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["type"]==PoliciesTypes.REQUEST_TWEET_RETWEET:
            '''
            bot_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["type"]==PoliciesTypes.REQUEST_TWEET_REPLY:
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
        elif msg["type"]==PoliciesTypes.REQUEST_FOLLOW_USER:
            '''
            bot_id
            tweet_user_id
            '''
            query=""
        else:
            return self.send_response({"response":"DENY"})

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
        