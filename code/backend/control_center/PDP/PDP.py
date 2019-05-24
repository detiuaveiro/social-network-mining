import json
import psycopg2
import random
import sys
sys.path.append('../')
from Neo4j.neo4j_api import Neo4jAPI
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
        self.neo=Neo4jAPI()
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
        msg={"type":action,data}
        '''
        evaluate_answer=False

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
            user_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["type"]==PoliciesTypes.REQUEST_TWEET_RETWEET:
            '''
            bot_id
            user_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            return self.send_response({"response":"PERMIT"})
        elif msg["type"]==PoliciesTypes.REQUEST_TWEET_REPLY:
            '''
            bot_id 
            user_id       
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

            workflow of this request:

            1- Check bot and its policies
                1.1- if filter=target and target=tweet_user_id:
                        return PERMIT
                1.2- if other_bots.filter=target and other_bots.target=tweet_user_id:
                        return DENY
                1.3- No one has this target
                        GOTO Rule 2
            
            2- Check neo4j
                2.1- Bot already follows tweet_user_id (this case should never happen, just here for precaution)
                        return DENY
                2.2- Other bot is following tweet_user_id: (questionable, should be discussed)
                        return DENY
                2.3- No one follows tweet_user_id:
                        return PERMIT
            '''
            query="select params from policies,filter where policies.active=TRUE and policies.filter=filter.id and filter.name=Target"
            cur=self.conn.cursor()
            try:
                '''
                Rule 1
                '''
                cur.execute(query)
                DB_val=cur.fetchall()
                self.conn.commit()
                
                #probably don't need this postProcess, since all logic is handled here
                #data=self.postProcess(num,DB_val)
                
                #apply the heuristics here
                for i in DB_val:
                    params=i[0]
                    if params[0]==msg["tweet_user_id"]:
                        for j in params[1:]:
                            if j==msg["bot_id"]:
                                return self.send_response({"response":"PERMIT"})
                '''
                Rule 2
                '''
                if self.neo.search_relationship(msg["tweet_user_id"],msg["bot_id"]):
                    return self.send_response({"response":"DENY"})
                #Rule 2.2 not implemented (maybe in the future?)
                else:
                    return self.send_response({"response":"PERMIT"})
            except psycopg2.Error:
                self.conn.rollback()
                evaluate_answer=False
            finally:
                cur.close()
                self.conn.close()

        elif msg["type"]==PoliciesTypes.FIRST_TIME:
            '''
            bot_id
            
            workflow of this request:

            new user arrives the jungle. he is presented with some fine-grained users to start analyzing
            
            Returns:
                random number of users to follow, and random users to follow in a dictionary {args : [] }.
            '''
            lista=self.get_suggested_users()
            return self.send_response({"args":lista})
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
    
    def get_suggested_users(self):
        '''
        num_users: Random number of users to start following
        usernames: List of usernames to return to the bot
        '''
        num_users=random.randint(2,10)
        usernames=[]
        users=["dailycristina","PaulaNevesD","doloresaveiro","Corpodormente","Manzarra","Feromonas","DanielaRuah","RicardoTPereira","LuciaMoniz","D_Morgado","ClaudiaPFVieira","RuiSinelCordes","DiogoBeja","blackmirror","13ReasonsWhy","NetflixPT","DCComics","gameofthrones","cw_arrow","CW_TheFlash","TheCW_Legends","nbcthisisus","lacasadepapel","lucifernetflix","thecwsupergirl","cw_riverdale","hawaiifive0cbs","cwthe100","agentsofshield","thesimpsons","macgyvercbs","americancrimetv","acsfx","shadowhunterstv","theamericansfx","crimminds_cbs","KimKardashian","khloekardashian","kourtneykardash","KendallJenner","KylieJenner","KrisJenner","pewdiepie","tim_cook","elonmusk","BillGates","FCPorto","KDTrey5","Cristiano","hazardeden10","PauDybala_JR","Sporting_CP","Dame_Lillard","stephenasmith","RealSkipBayless","ManCity","juventusfc","FCBarcelona","realmadrid","SergioRamos","KingJames","katyperry","cher","NICKIMINAJ","deadmau5","kanyewest","axlrose","patrickcarney","vincestaples","KillerMike","thedavidcrosby","samantharonson","Eminem","pittyleone","thesonicyouth","bep","ladygaga","coldplay","britneyspears","backstreetboys","chilipeppers","fosterthepeople","acdc","arcticmonkeys","blurofficial","gorillaz","greenday","linkinpark","MCRofficial","falloutboy","PanicAtTheDisco","AllTimeLow","PTXofficial","kirstin","StephenCurry30","NBA","SLBenfica","partido_pan","ppdpsd","psocialista","_cdspp","cdupcppev","realdonaldtrump","borisjohnson","nigel_farage","jeremycorbyn","theresa_may","joebiden","fhollande","angelamerkeicdu","barackobama","berniesanders","nicolasmaduro","vp","realxi_jinping","mlp_officiel","jguaido","RuiRioPSD","antoniocostapm","catarina_mart","cristasassuncao","heloisapolonia","jairbolsonaro"]
        while num_users>0:
            num=random.randint(0,len(users)-1)
            usernames.append(users[num])
            num_users-=1
        for i in usernames:
            for j in usernames:
                if i==j:
                    usernames.remove(j)
        return usernames