# Useful stuff for mongo

BLANK_TWEET = {
	"id": "",
	"text": "",
	"truncated": False,
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [],
		"urls": []
	},
	"source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
	"in_reply_to_status_id": None,
	"in_reply_to_user_id": None,
	"in_reply_to_screen_name": None,
	"user": "",
	"is_quote_status": False,
	"retweet_count": 0,
	"favorite_count": 0,
	"lang": "",
	"is_blank": True
}

BLANK_USER = {
	"id": 0,
	"id_str": "",
	"name": "",
	"screen_name": "",
	"location": "",
	"description": "",
	"url": "",
	"protected": False,
	"followers_count": 0,
	"friends_count": 0,
	"listed_count": 0,
	"favourites_count": 0,
	"verified": False,
	"statuses_count": 0,
	"lang": None,
	"contributors_enabled": False,
	"profile_background_color": "#FFFFFF",
	"profile_background_image_url": "",
	"profile_background_image_url_https": "",
	"profile_background_tile": False,
	"profile_image_url": "",
	"profile_image_url_https": "",
	"profile_link_color": "#FFFFFF",
	"profile_sidebar_border_color": "#FFFFFF",
	"profile_sidebar_fill_color": "#FFFFFF",
	"profile_text_color": "#FFFFFF",
	"profile_use_background_image": False,
	"has_extended_profile": False,
	"default_profile": False,
	"default_profile_image": False,
	"following": False,
	"follow_request_sent": False,
	"notifications": False,
	"is_blank": True
}

BLANK = "blank"
NOT_BLANK = "normal"
