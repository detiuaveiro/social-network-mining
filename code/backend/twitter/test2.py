from control_center.control_center import Control_Center

cc = Control_Center()

# First we must test that it's inserting tweets on neo4j when everything's normal
tweet = {
	"id" : 12332345,
	"text" : "RT @nbastats: HISTORY!\n\nSteph Curry and Draymond Green become the first teammates in @NBAHistory to both record a triple-double in the same…",
	"truncated" : False,
	"entities" : {
		"hashtags" : [ ],
		"symbols" : [ ],
		"user_mentions" : [],
		"urls" : [ ]
	},
	"source" : "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id" : None,
	"in_reply_to_user_id" : None,
	"in_reply_to_screen_name" : None,
	"user" : 123522625,
	"is_quote_status" : False,
	"retweet_count" : 564,
	"favorite_count" : 0,
	"lang" : "en"
}

cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})

# Check if replying creates both nodes

tweet = {
	"id" : 87654324,
	"text": "You might like this too, if you love this band as much as I do https://t.co/KiqPorHLua",
	"truncated": False,
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [],
		"urls": [ ]
	},
	"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id": 3252352,
	"in_reply_to_user_id": 8078996,
	"in_reply_to_screen_name": "coldplay",
	"user": 82734234,
	"is_quote_status": False,
	"retweet_count": 165,
	"favorite_count": 1628,
	"possibly_sensitive": False,
	"lang": "en"
}

cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})

# Check if quoting creates both nodes
tweet ={
	"id" : 57489572963,
	"text" : "💗💙 PH https://t.co/CS0t6dUuFa",
	"truncated" : False,
	"entities" : {
		"hashtags" : [ ],
		"symbols" : [ ],
		"user_mentions" : [ ],
		"urls" : [
			{
				"url" : "https://t.co/CS0t6dUuFa",
				"expanded_url" : "https://twitter.com/_FiercePanda/status/1121788296454004737",
				"display_url" : "twitter.com/_FiercePanda/s…",
				"indices" : [
					6,
					29
				]
			}
		]
	},
	"source" : "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id" : None,
	"in_reply_to_user_id" : None,
	"in_reply_to_screen_name" : None,
	"user" : 104728563,
	"is_quote_status" : True,
	"quoted_status_id" : 72305235235,
	"quoted_author_id": 120957283,
	"retweet_count" : 397,
	"favorite_count" : 3161,
	"possibly_sensitive" : False,
	"lang" : "und"
}

cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})


cc.close()