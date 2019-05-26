import json
import psycopg2
import random
import sys
import datetime
from pymongo import MongoClient
sys.path.append('../')
from Neo4j.neo4j_api import Neo4jAPI
from Postgres.postgreSQL import postgreSQL_API
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
        self.PoliciesTypes=PoliciesTypes(4)
        self.neo=Neo4jAPI()
        self.policies=postgreSQL_API()
        self.client=MongoClient('mongodb://192.168.85.46:32769/')
        self.users=self.client.twitter.users
        self.tweets=self.client.twitter.tweets
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
        for all REQUEST_TWEET*, it's based on a heuristic (if it's in the threshold, request accepted): 0 to 1
        if it's a REQUEST_FOLLOW_USER, check the rules to see if it is accepted
        if it's a first time user, give some usernames
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
            res=self.analyze_tweet_like(msg)
            if res>0.4:
                return self.send_response({"response":"PERMIT"})
            else:
                return self.send_response({"response":"DENY"})
        elif msg["type"]==PoliciesTypes.REQUEST_TWEET_RETWEET:
            '''
            bot_id
            user_id
            tweet_id
            tweet_text
            tweet_entities
                - from entities, fetch hashtags and mentions
            '''
            res=self.analyze_tweet_retweet(msg)
            if res>0.6:
                return self.send_response({"response":"PERMIT"})
            else:
                return self.send_response({"response":"DENY"})
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
            res=self.analyze_tweet_reply(msg)
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
            evaluate_answer=self.analyze_follow_user(msg)

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
            
    def send_response(self,msg):
        #json dumps da decisão
        message=json.dumps(msg)
        self.policies.closeConnection()
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
    
    def analyze_follow_user(self,msg):
        '''
        Rule 1
        '''
        DB_val=self.policies.getPoliciesParams()
        if DB_val=='ERROR':
            return self.send_response({"response":"DENY"})
        #probably don't need postProcess, since all logic is handled here
        
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
    
    def analyze_tweet_like(self,msg):
        threshold=0
        '''
        msg={
            bot_id
            user_id 
            tweet_id
            tweet_text
            tweet_entities- from entities, fetch hashtags and mentions
            }
        0.4 to pass
        follows the user: +0.3
        policy target on that user: +0.4
        retweeted that tweet: +0.2
        policy keywords checks out: +0.2
        already liked too many tweets from that user in a row (2 || 3): -0.35
        already liked too many tweets from that user in a row (4 || 5): -0.65
        '''
        follow=self.neo.search_relationship(msg["user_id"],msg["bot_id"])
        if follow:
            threshold+=0.3
        lista=self.policies.getPoliciesByBot(msg["bot_id"])
        val=False
        for i in lista:
            if i["filter"]=="Target":
                '''
                analisar tweet_entities, user_id
                iterate over tweet_entities.user_mentions.id
                '''
                val=False
                params=i["params"]
                #if mentioned user is in the parameters, then ++
                for j in msg["tweet_entities"]["user_mentions"]:
                    if j["id_str"] in params:
                        val=True
                        break
                #if user is in the parameters, then ++
                if msg["user_id"] in params:
                        val=True
                
                if val:
                    threshold+=0.4        
            elif i["filter"]=="Keywords":
                '''
                analisar tweet_entities, tweet_text
                iterate over tweet_entities.hashtags.text
                '''
                val=False
                for j in msg["tweet_entities"]["hashtags"]:
                    if j["text"] in i["params"]:
                        val=True
                        break
                for k in i["params"]:
                    if k in msg["tweet_text"]:
                        val=True
                        break
                if val:
                    threshold+=0.2
        val=False
        logs=self.policies.searchLog(msg["bot_id"])
        for i in range(len(logs)-1):
            action=logs[i]["action"]
            if "TWEET RETWEETED" in action:
                sp=action.split("ID: ")
                spp=sp[1].split(" )")
                id_tweet=spp[0]
                if id_tweet==msg["tweet_id"]:
                    val=True
                    break
        if val:
            if threshold==0.9:
                threshold=1
            else:
                threshold+=0.2

        for j in range(len(logs)-1):
            action=logs[i]["action"]
            if "TWEET LIKED" in action:
                sp=action.split("ID: ")
                spp=sp[1].split(" )")
                id_tweet=spp[0]
                
                id_user=self.tweets.find_one({"id":id_tweet},{"user":1,"_id":0})
                if msg["user_id"]==id_user:
                    date=logs[i]["timestamp"]
                    now=datetime.datetime.now()
                    if (now-date).seconds<30:
                        threshold-=0.65
                    elif (now-date).seconds<60:
                        threshold-=0.35
        return threshold

    def analyze_tweet_retweet(self,msg):
        threshold=0
        '''
        msg={
            bot_id
            user_id 
            tweet_id
            tweet_text
            tweet_entities- from entities, fetch hashtags and mentions
            }
        0.6 to pass
        follows the user: +0.3
        policy target on that user: +0.4
        liked that tweet: +0.3
        policy keywords checks out: +0.2
        already retweeted recently from that user (1 || 2) (12h): -0.5
        '''
        follow=self.neo.search_relationship(msg["user_id"],msg["bot_id"])
        if follow:
            threshold+=0.3
        lista=self.policies.getPoliciesByBot(msg["bot_id"])
        val=False
        for i in lista:
            if i["filter"]=="Target":
                '''
                analisar tweet_entities, user_id
                iterate over tweet_entities.user_mentions.id
                '''
                val=False
                params=i["params"]
                #if mentioned user is in the parameters, then ++
                for j in msg["tweet_entities"]["user_mentions"]:
                    if j["id_str"] in params:
                        val=True
                        break
                #if user is in the parameters, then ++
                if msg["user_id"] in params:
                        val=True
                
                if val:
                    threshold+=0.4        
            elif i["filter"]=="Keywords":
                '''
                analisar tweet_entities, tweet_text
                iterate over tweet_entities.hashtags.text
                '''
                val=False
                for j in msg["tweet_entities"]["hashtags"]:
                    if j["text"] in i["params"]:
                        val=True
                        break
                for k in i["params"]:
                    if k in msg["tweet_text"]:
                        val=True
                        break
                if val:
                    threshold+=0.2
        val=False
        logs=self.policies.searchLog(msg["bot_id"])
        for i in range(len(logs-1)):
            action=logs[i]["action"]
            if "TWEET LIKED" in action:
                sp=action.split("ID: ")
                spp=sp[1].split(" )")
                id_tweet=spp[0]
                if id_tweet==msg["tweet_id"]:
                    val=True
                    break
        if val:
            if threshold==0.9:
                threshold=1
            else:
                threshold+=0.3
        
        for j in range(len(logs)-1):
            action=logs[i]["action"]
            if "TWEET RETWEETED" in action:
                sp=action.split("ID: ")
                spp=sp[1].split(" )")
                id_tweet=spp[0]
                
                id_user=self.tweets.find_one({"id":id_tweet},{"user":1,"_id":0})
                if msg["user_id"]==id_user:
                    date=logs[i]["timestamp"]
                    now=datetime.datetime.now()
                    #12h -> 43200s
                    if (now-date).seconds<43200:
                        threshold-=0.5

        return threshold
    def analyze_tweet_reply(self,msg):
        return "not implemented yet"
