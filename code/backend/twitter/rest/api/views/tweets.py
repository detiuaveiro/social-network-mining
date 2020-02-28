from ..

def twitter_tweets(request):
	lim = request.args.get("limit")
	if lim is None:
		mapa = mongo_t.twitterCollection()
	else:
		try:
			lim = int(lim)
			mapa = mongo_t.twitterCollection(limite=lim)
		except TypeError:
			return app.response_class(json.dumps({"Error": "Limit must be an integer!"}), status=400,
									  mimetype="application/json")
	for i in mapa:
		i["id"] = str(i["id"])
		i["user"] = str(i["user"])
		if i["is_quote_status"]:
			try:
				i["quoted_status_id"] = str(i["quoted_status_id"])
			except KeyError:
				pass
		if type(i["in_reply_to_screen_name"]) is str:
			i["in_reply_to_user_id"] = str(i["in_reply_to_user_id"])
			i["in_reply_to_status_id"] = str(i["in_reply_to_status_id"])
	return jsonify(mapa)


def twitter_tweets_export(request):
	return None


def twitter_tweets_stats(request):
	return None


def twitter_tweet(request, id):
	return None


def twitter_tweet_stats(request, id):
	return None


def twitter_tweet_replies(request, id):
	return None
