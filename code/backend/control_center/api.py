from flask import Flask,url_for
import json

app=Flask(__name__)

@app.route("/")
def home():
    return "<h1>root</h1>"

@app.route("/stats")
def stats():
    return "<h1>stats</h1>"

@app.route("/bots")
def bots():
    return "<h1>bots</h1>"

@app.route("/policies")
def policies():
    return "<h1>policies</h1>"

@app.route("/network")
def network():
    return "<h1>network</h1>"


if __name__ == "__main__":
    app.run(debug=True)