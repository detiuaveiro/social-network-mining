from flask import Flask, jsonify, json, request, send_file
from mongo_api import MongoAPI
from markovify import markovify

app=Flask(__name__)

mongo = MongoAPI()

@app.route("/generate/tweet/<id>")
def user_tweets(id):
    tweets = mongo.getTweets(id)
    text = ""
    for tweet in tweets:
        text += tweet["text"]+"\n"
    text_model = markovify.Text(text)
    return text_model.make_short_sentence(280)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
