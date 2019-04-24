from flask import Flask,url_for, Response, jsonify, json

app=Flask(__name__)

#mongo.insertOneData(2, ["porto", "desporto"], "abilio", "o porto foi um justo vencedor!")

f=open("/home/user/Transferências/file.json","r+")

json_to_send=json.load(f)

@app.route("/")
def home():
    return "<h1>root</h1>"

@app.route("/twitter/users")
def user_general():
    users = json_to_send["users"]
    data = [v for i,v in users.items()]
    for i in data:
        user_id=str(i["id"])
        i.pop("id")
        i["id"] = user_id
    return jsonify(data) #Response(json.dumps(data),mimetype='application/json')
    #return "<h1>"+ str(mongoUsers.dataCollection()) + "</h1>"

@app.route("/twitter/users/stats")
def user_general_stats():
    #stand by
    return "user stats"

@app.route("/twitter/users/<id>")
def user_by_id(id):
    try:
        user_id = str(json_to_send["users"][id]["id"])
        json_to_send["users"][id].pop("id")
        json_to_send["users"][id]["id"] = user_id
        user = json_to_send["users"][id]
        return jsonify(user)
    except KeyError:
        return jsonify({"id":"not found"})
    #return "<h1>"+ str(mongoUsers.dataCollection(findText={"id":int(id)})) + "</h1>"

@app.route("/twitter/users/<id>/tweets")
def user_tweets(id):
    #query nos tweets a procurar pelo id=id
    #retornar json com os tweets
    return "user tweets"

@app.route("/twitter/users/<id>/followers")
def user_followers(id):
    followers = json_to_send["users"][id]["followers_count"]
    return jsonify(followers)
    

@app.route("/twitter/users/<id>/following")
def user_following(id):
    #como fazer com o following???
    #return json.dumps(json_to_send["users"][id]["followers_count"])
    return "user following"

@app.route("/twitter/users/<id>/replies")
def user_replies(id):
    #query nos tweets a procurar pelo id=id
    #retornar json com os replies
    return "user replies"

@app.route("/twitter/users/<id>/stats")
def user_stats(id):
    #stand by
    return "user stats"

'''
twitter paths
'''
@app.route("/twitter/network")
def tt_network():
    return "twitter"

@app.route("/twitter/policies")
def tt_policies():
    return "twitter"

@app.route("/twitter/stats")
def tt_stats():
    return "twitter"

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
    tweets = json_to_send["tweets"]
    data = [v for i,v in tweets.items()]
    return jsonify(data)
    #return "<h1>"+ str(mongoTweets.dataCollection()) + "</h1>"


@app.route("/twitter/tweets/stats")
def tt_tweet_stats():
    #agregação de likes, retweets
    return "twitter"

@app.route("/twitter/tweets/<id>")
def tt_tweet_by_id(id):
    tweet=json_to_send["tweets"][id]
    return jsonify(tweet)
    #return "<h1>"+ str(mongoTweets.dataCollection(findText={"id":int(id)})) + "</h1>"

@app.route("/twitter/tweets/<id>/stats")
def tt_tweet_stats_by_id(id):
    rt_count=json_to_send["tweets"][id]["retweet_count"]
    fav_count=json_to_send["tweets"][id]["favorite_count"]
    data = [{"retweet_count":rt_count,"favorite_count":fav_count}]
    return jsonify(data)

'''
policies paths
'''
@app.route("/policies")
def policies():
    return "<h1>policies</h1>"

@app.route("/policies/<id>")
def policies_by_id(id):
    return "<h1>policies by id</h1>"

@app.route("/policies/bots/<id>")
def policies_by_bot(id):
    return "<h1>policies by bot</h1>"
##########################################################################################################################
'''
instagram paths
'''
@app.route("/instagram/policies")
def ig_policies():
    return "ig policies"

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

@app.route("/twitter/network")
def network():
    return "<h1>network</h1>"


@app.route("/timescale")
def timescale():
    return "<h1>timescale</h1>"


if __name__ == "__main__":
    app.run(debug=True)
