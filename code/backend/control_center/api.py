from flask import Flask,url_for, Response, jsonify, json
from mongo_flask import AppMongo
from postgreSQL import postgreSQLConnect

app=Flask(__name__)

mongo=AppMongo(app,"users")
mongo_t=AppMongo(app,"tweets")
postgres=postgreSQLConnect()
timescale=postgres.connect("postgres")
policy=postgres.connect("policies")
'''/
    users
        user
            user_info
    tweets
        tweet
            tweet_info
'''

@app.route("/")
def home():
    return "root"

@app.route("/twitter/users")
def user_general():
    
    mapa=mongo.dataCollection()
    for i in mapa:
        user_id=str(i["id"])
        i.pop("id")
        i["id"] = user_id
    return jsonify(mapa)

##################################################################################    
@app.route("/twitter/users/stats")
def user_general_stats():
    #stand by
    return "user stats"
##################################################################################

@app.route("/twitter/users/<id>")
def user_by_id(id):
    
    try:
        mapa=mongo.dataCollection(findText={"id":int(id)})
        if len(mapa)>0:
            mapa[0].pop("id")
            mapa[0]["id"]=(str(id))
            return jsonify(mapa)
        else:
            return jsonify({"Error":"wrong id"})
    except TypeError:
        return jsonify({"Error":"invalid"})

@app.route("/twitter/users/<id>/tweets")
def user_tweets(id):
    mapa=mongo_t.dataCollection(findText={"user.id_str":str(id)})
    return jsonify(mapa)

@app.route("/twitter/users/<id>/followers")
def user_followers(id):
    
    followers = mongo.getOneFilteredDoc(findText={"id":int(id)},projection={"followers_count":True,"_id":False})
    return jsonify(followers)
    
@app.route("/twitter/users/<id>/following")
def user_following(id):
    mapa=mongo.getOneFilteredDoc(findText={"id":int(id)},projection={"friends_count":True,"_id":False})
    return jsonify(mapa)

##################################################################################
'''
Check the objective of this path first. Could be:
    - All replies from the user
    - Count of all the replies from the user
'''
'''
The relevant fields in a reply tweet are in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_screen_name, in_reply_to_user_id, in_reply_to_user_id_str.
The names of each of these fields reasonably describe their contents. 
The most significant of these is in_reply_to_status_id, which supports finding the tweet to which the reply tweet is a reply.
'''
@app.route("/twitter/users/<id>/replies")
def user_replies(id):
    mapa=mongo_t.dataCollection(findText={"in_reply_to_user_id_str":str(id)})
    return jsonify(mapa)
##################################################################################

@app.route("/twitter/users/<id>/stats")
def user_stats(id):
    stats=mongo.getOneFilteredDoc(findText={"id":int(id)},projection={"favourites_count":True,"followers_count":True,"friends_count":True,"location":True,"name":True,"screen_name":True,"statuses_count":True,"verified":True,"_id":False})
    return jsonify(stats)

'''
twitter paths
'''
@app.route("/twitter/network")
def tt_network():
    return "twitter"

@app.route("/twitter/policies")
def tt_policies():
    mapa=policy.getPoliciesByAPI("twitter")
    return jsonify(mapa)

##################################################################################
@app.route("/twitter/stats")
def tt_stats():
    return "twitter"
##################################################################################

@app.route("/twitter/bots")
def tt_bots():
    return "TBD" #json.dumps(json_to_send["users"]["1103294806497902594"])

@app.route("/twitter/bots/<id>")
def tt_bots_by_id(id):
    #if id=="1103294806497902594":
    #    return json.dumps(json_to_send["users"][id])
    return "twitter"

@app.route("/twitter/bots/<id>/logs")
def tt_bot_logs(id):
    return "TBD"

@app.route("/twitter/tweets")
def tt_tweets():
    
    mapa=mongo_t.dataCollection()
    return jsonify(mapa)

##################################################################################
@app.route("/twitter/tweets/stats")
def tt_tweet_stats():
    #agregação de likes, retweets
    pipeline=[{'$project':{
        'favorite': {'$sum': '$favorite_count'},
        'retweet': {'$sum': '$retweet_count'}}}]

    mapa=mongo_t.aggregate(pipeline)
    fav=0
    ret=0
    for i in mapa:
        fav+=i["favorite"]
        ret+=i["retweet"]
    return jsonify({"favorite_count":fav,"retweet_count":ret})
##################################################################################

@app.route("/twitter/tweets/<id>")
def tt_tweet_by_id(id):
    try:
        mapa=mongo_t.dataCollection(findText={"id":int(id)})
        return jsonify(mapa)
    except TypeError:
        return jsonify({"Error":"invalid"})
    
    
@app.route("/twitter/tweets/<id>/stats")
def tt_tweet_stats_by_id(id):
    mapa=mongo_t.getOneFilteredDoc(findText={"id":int(id)},projection={"created_at":True,"entities.hashtags":True,"entities.user_mentions.name":True,"entities.user_mentions.screen_name":True,"favorited":True,"in_reply_to_screen_name":True,"in_reply_to_status_id_str":True,"in_reply_to_user_id_str":True,"is_quote_status":True,"place":True,"favorite_count":True,"retweet_count":True,"retweeted":True,'user.id_str':True,'user.name':True,'user.screen_name':True,'_id':False})
    return jsonify(mapa)

'''
policies paths
'''
@app.route("/policies")
def policies():
    mapa=policy.getAllPolicies()
    return jsonify(mapa)

@app.route("/policies/<id>")
def policies_by_id(id):
    mapa=policy.getPoliciesByID(id)
    return jsonify(mapa)

@app.route("/policies/bots/<id>")
def policies_by_bot(id):
    mapa=policy.getPoliciesByBot(id)
    return jsonify(mapa)

@app.route("/policies/add")
def add_policy():
    '''
    This function receives all the information needed to create a policy.
    It is stored in a list and then is sent to the db
    Returns the json with the response from the database:
        - Inserted successfully
        - Error (returns the driver's specific error)
    '''
    lista=[]
    send=policy.addPolicy(lista)
    return jsonify(send)

@app.route("/policies/remove/<id>")
def remove_policy(id):
    '''
    This function gets the id of the policy to be removed and queries the db for its removal.
    Returns the json with the response from the database:
        - Removed successfully
        - Error (returns the driver's specific error)
    '''
    send=policy.removePolicy(id)
    return jsonify(send)
##################################################################################################################################
'''
instagram paths
'''
@app.route("/instagram/policies")
def ig_policies():
    mapa=policy.getPoliciesByAPI("instagram")
    return jsonify(mapa)

@app.route("/instagram/stats")
def ig_stats():
    return "ig stats"

@app.route("/instagram/bots")
def ig_bots_general():
    return "bots"

@app.route("/instagram/bots/<int:id>/")
def bot_by_id(id):
    return "bot by id"

@app.route("/instagram/bots/<int:id>/logs")
def bot_logs(id):
    return "bot logs"


if __name__ == "__main__":
    app.run(debug=True)
