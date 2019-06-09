from flask import Flask, jsonify, json, request, send_file
from flask_cors import CORS
from Mongo.mongo_flask import AppMongo
from Postgres.postgreSQL import postgreSQL_API
from Neo4j.neo4j_api import Neo4jAPI
from send import RabbitSend
import ast
from ElasticSearch.ElasticSearch import getESService

app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

mongo = AppMongo(app, "users")
mongo_t = AppMongo(app, "tweets")
postgres = postgreSQL_API("postgres")
policy = postgreSQL_API("policies")
neo = Neo4jAPI()
elas=getESService()
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
    mapa = mongo.dataCollection()
    for i in mapa:
        i["id"] = str(i["id"])
    return jsonify(mapa)


@app.route("/twitter/users/stats")
def user_general_stats():
    stats = postgres.getAllStatsUsers()
    return jsonify(stats)


@app.route("/twitter/users/<id>")
def user_by_id(id):
    try:
        mapa = mongo.dataCollection(findText={"id": int(id)})
        if len(mapa) > 0:
            mapa[0]["id"] = (str(id))
            return app.response_class(response=json.dumps(mapa), status=200,
                                      mimetype='application/json')  # jsonify(mapa)
        else:
            return app.response_class(response=json.dumps({"Error": "wrong id"}), status=400,
                                      mimetype='application/json')
    except TypeError:
        return app.response_class(response=json.dumps({"Error": "invalid"}), status=400,
                                  mimetype='application/json')


@app.route("/twitter/users/<id>/tweets")
def user_tweets(id):
    mapa = mongo_t.twitterCollection(findText={"user": id})
    for i in mapa:
        i["id"]=str(i["id"])
    return jsonify(mapa)


@app.route("/twitter/users/<id>/followers")
def user_followers(id):
    followers = neo.get_followers(id)
    lista = []
    for i in followers:
        lista.append(i[0])
    return jsonify(lista)


@app.route("/twitter/users/<id>/following")
def user_following(id):
    users = neo.get_following(id)
    lista = []
    for i in users:
        lista.append(i[0])
    return jsonify(lista)

'''
The relevant fields in a reply tweet are in_reply_to_status_id_str, in_reply_to_screen_name, in_reply_to_user_id_str.
The most significant of these is in_reply_to_status_id, which supports finding the tweet to which the reply tweet is a reply.
'''

@app.route("/twitter/users/<id>/replies")
def user_replies(id):
    mapa = mongo_t.twitterCollection(
        findText={ "$or": [ {"in_reply_to_user_id_str": str(id)}, {"in_reply_to_screen_name": str(id)}, {"in_reply_to_status_id_str":str(id)} ]})
    return jsonify(mapa)



@app.route("/twitter/users/<id>/stats")
def user_stats(id):
    stats = postgres.getStatsUserID(id)
    return jsonify(stats)


'''
twitter paths
'''


@app.route("/twitter/network")
def tt_network():
    return "bolt://192.168.85.187:7687"

@app.route("/twitter/network/export")
def export_network():
    neo.export_network()
    return jsonify({"Message":"Success"})

@app.route("/twitter/policies")
def tt_policies():
    mapa = policy.getPoliciesByAPI("Twitter")
    return jsonify(mapa)


@app.route("/twitter/create", methods=['POST'])
def tt_create():
    if request.method == 'POST':
        mapa = request.data.decode('utf-8')
        mapa = ast.literal_eval(mapa)
        print(mapa)
        for bot in mapa["bots"]:
            if mapa["timeline"]:
                payload = {
                    "type": 5,
                    "params": {
                        "status": mapa["status"],
                    }
                }
            else:
                payload = {
                    "type": 5,
                    "params": {
                        "status": mapa["status"],
                        "in_reply_to_status_id": mapa["in_reply_to_status_id"],

                    }
                }
            try:
                conn = RabbitSend(host='192.168.85.185', port=5672, vhost="PI",
                                        username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
                conn.send(routing_key='tasks.twitter.' + bot, message=payload)
                conn.close()                
                return jsonify({"Message": "Success"})
            except Exception as e:
                return app.response_class(response=json.dumps({"Message": "Bad Tweet Request"}), status=400,
                                                mimetype='application/json')


@app.route("/twitter/stats")
def tt_stats():
    stats = postgres.getAllStats()
    return jsonify(stats)


@app.route("/twitter/bots")
def tt_bots():
    val = neo.search_all_bots()
    '''
    Fazer integração de resultados com o mongoDB
    '''
    lista = []
    swap = []
    for i in val:

        temp = mongo.dataCollection(findText={"id": int(i["id"])})
        lista.append(temp)

    for i in lista:
        for j in i:
            swap.append(j)

    for j in swap:
        j["id"] = str(j["id"])

    return jsonify(swap)


@app.route("/twitter/bots/<id>")
def tt_bots_by_id(id):
    val = neo.search_bot_by_id(id)
    return jsonify(val)


@app.route("/twitter/bots/<id>/logs")
def tt_bot_logs(id):
    val = policy.searchLog(id)
    return jsonify(val)


@app.route("/twitter/tweets")
def tt_tweets():
    mapa = mongo_t.twitterCollection()
    for i in mapa:
        i["id"] = str(i["id"])
    return jsonify(mapa)

@app.route("/twitter/tweets/export")
def export_tweets():
    a=mongo_t.exportTweets(fields={"entities":True,"favorite_count":True},export_type="csv")
    if type(a)==dict:
        return jsonify(a)
    else:
        return send_file("/home/user/Documents/proj_PI/social-network-mining/code/backend/control_center/data.csv",attachment_filename="data.csv")

@app.route("/twitter/tweets/stats")
def tt_tweet_stats():
    stats = elas.getAllStatsTweets(length=50)

    return jsonify(stats)


@app.route("/twitter/tweets/<id>")
def tt_tweet_by_id(id):
    try:
        mapa = mongo_t.twitterCollection(findText={"id": int(id)})
        for i in mapa:
            i["id"] = str(i["id"])
        return jsonify(mapa)
    except TypeError:
        return app.response_class(response=json.dumps({"Error": "invalid"}), status=400,
                                  mimetype='application/json')


@app.route("/twitter/tweets/<id>/stats")
def tt_tweet_stats_by_id(id):
    # mapa=mongo_t.getOneFilteredDoc(findText={"id":int(id)},projection={"created_at":True,"entities.hashtags":True,"entities.user_mentions.name":True,"entities.user_mentions.screen_name":True,"favorited":True,"in_reply_to_screen_name":True,"in_reply_to_status_id_str":True,"in_reply_to_user_id_str":True,"is_quote_status":True,"place":True,"favorite_count":True,"retweet_count":True,"retweeted":True,'user.id_str':True,'user.name':True,'user.screen_name':True,'_id':False})
    stats = postgres.getStatsTweetID(id)
    return jsonify(stats)


'''
policies paths
'''


@app.route("/policies")
def policies():
    mapa = policy.getAllPolicies()
    return jsonify(mapa)


@app.route("/policies/<id>")
def policies_by_id(id):
    mapa = policy.getPoliciesByID(id)
    return jsonify(mapa)


@app.route("/policies/bots/<id>")
def policies_by_bot(id):
    mapa = policy.getPoliciesByBot(id)
    return jsonify(mapa)


@app.route("/policies/add", methods=['POST'])
def add_policy():
    '''
    This function receives all the information needed to create a policy.
    It is stored in a dictionary and then is sent to the db
    Returns the json with the response from the database:
        - 200 Inserted successfully
        - 400 Error (returns the driver's specific error)
    '''
    if request.method == 'POST':
        mapa = request.data.decode('utf-8')
        mapa = ast.literal_eval(mapa)
        print(mapa)
        send = policy.addPolicy(mapa)
        if "Message" not in send.keys():
            return app.response_class(response=json.dumps(send), status=400,
                                      mimetype='application/json')
        return jsonify(send)


@app.route("/policies/remove/<id>", methods=['DELETE', 'POST'])
def remove_policy(id):
    '''
    This function gets the id of the policy to be removed and queries the db for its removal.
    Returns the json with the response from the database:
        - 200 Removed successfully
        - 400 Error (returns the driver's specific error)
    '''
    if request.method == 'DELETE':
        send = policy.removePolicy(id)
        if "Message" not in send.keys():
            return app.response_class(response=json.dumps(send), status=400,
                                      mimetype='application/json')
        return jsonify(send)

    if request.method == 'POST':
        send = policy.removePolicy(id)
        if "Message" not in send.keys():
            return app.response_class(response=json.dumps(send), status=400,
                                      mimetype='application/json')
        return jsonify(send)


@app.route("/policies/update", methods=['POST'])
def update_policy():
    '''
    Update a policy. Sends a dictionary with the columns and respective values that are going to be updated. 
    Returns the json with the response from the database:
        - 200 Updated successfully
        - 400 Error (returns the driver's specific error)
    '''
    # mapa -> dados recebidos da dashboard
    if request.method == 'POST':
        mapa = request.data.decode('utf-8')
        mapa = ast.literal_eval(mapa)
        send = policy.updatePolicy(mapa)
        if "Message" not in send.keys():
            return app.response_class(response=json.dumps(send), status=400,
                                      mimetype='application/json')
        return jsonify(send)


##################################################################################################################################

'''
instagram paths
'''


@app.route("/instagram/policies")
def ig_policies():
    mapa = policy.getPoliciesByAPI("Instagram")
    return jsonify(mapa)


@app.route("/instagram/stats")
def ig_stats():
    return "instagram stats"


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
    app.run(debug=True, host='0.0.0.0')
