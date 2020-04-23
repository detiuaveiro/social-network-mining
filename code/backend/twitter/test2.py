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
	"created_at" : "Fri Apr 17 03:08:26 +0000 2020",
	"id" : 1250984437539536896,
	"id_str" : "1250984437539536896",
	"text" : "Kyrie Career-high 57 Trivia Answers:\n\n1) 7-7 from 3-point land\n2) Career-high 18 assists\n3) 6x NBA All-Star\n4) Rod Strickland",
	"truncated" : False,
	"entities" : {
		"hashtags" : [ ],
		"symbols" : [ ],
		"user_mentions" : [ ],
		"urls" : [ ]
	},
	"source" : "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
	"in_reply_to_status_id" : 1250929414591983624,
	"in_reply_to_status_id_str" : "1250929414591983624",
	"in_reply_to_user_id" : 19923144,
	"in_reply_to_user_id_str" : "19923144",
	"in_reply_to_screen_name" : "NBA",
	"user" : 19923144,
	"geo" : None,
	"coordinates" : None,
	"place" : None,
	"contributors" : None,
	"is_quote_status" : False,
	"retweet_count" : 5,
	"favorite_count" : 73,
	"favorited" : False,
	"retweeted" : False,
	"lang" : "en"
}


cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})

# Check if quoting creates both nodes
tweet = {
	"created_at" : "Mon Apr 06 23:46:03 +0000 2020",
	"id" : 1247309624866463744,
	"id_str" : "1247309624866463744",
	"text" : "Tonight @BillieJoe's hanging out (virtually) with @FallonTonight for a special #FallonAtHome #NoFunMondays https://t.co/8bQr7rXVLU",
	"truncated" : False,
	"entities" : {
		"hashtags" : [
			{
				"text" : "FallonAtHome",
				"indices" : [
					79,
					92
				]
			},
			{
				"text" : "NoFunMondays",
				"indices" : [
					93,
					106
				]
			}
		],
		"symbols" : [ ],
		"user_mentions" : [
			{
				"screen_name" : "billiejoe",
				"name" : "Billie Joe Armstrong",
				"id" : 241264057,
				"id_str" : "241264057",
				"indices" : [
					8,
					18
				]
			},
			{
				"screen_name" : "FallonTonight",
				"name" : "The Tonight Show",
				"id" : 19777398,
				"id_str" : "19777398",
				"indices" : [
					50,
					64
				]
			}
		],
		"urls" : [
			{
				"url" : "https://t.co/8bQr7rXVLU",
				"expanded_url" : "https://twitter.com/FallonTonight/status/1247304550047981570",
				"display_url" : "twitter.com/FallonTonight/…",
				"indices" : [
					107,
					130
				]
			}
		]
	},
	"source" : "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
	"in_reply_to_status_id" : None,
	"in_reply_to_status_id_str" : None,
	"in_reply_to_user_id" : None,
	"in_reply_to_user_id_str" : None,
	"in_reply_to_screen_name" : None,
	"user" : 67995848,
	"geo" : None,
	"coordinates" : None,
	"place" : None,
	"contributors" : None,
	"is_quote_status" : True,
	"quoted_status_id" : 1247304550047981570,
	"quoted_status_id_str" : "1247304550047981570",
	"quoted_status" : {
		"created_at" : "Mon Apr 06 23:25:53 +0000 2020",
		"id" : 1247304550047981570,
		"id_str" : "1247304550047981570",
		"text" : "...also tonight, a musical performance of “I Think We’re Alone Now” by @billiejoe! #FallonAtHome",
		"truncated" : False,
		"entities" : {
			"hashtags" : [
				{
					"text" : "FallonAtHome",
					"indices" : [
						83,
						96
					]
				}
			],
			"symbols" : [ ],
			"user_mentions" : [
				{
					"screen_name" : "billiejoe",
					"name" : "Billie Joe Armstrong",
					"id" : 241264057,
					"id_str" : "241264057",
					"indices" : [
						71,
						81
					]
				}
			],
			"urls" : [ ]
		},
		"source" : "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
		"in_reply_to_status_id" : 1247283872494206981,
		"in_reply_to_status_id_str" : "1247283872494206981",
		"in_reply_to_user_id" : 19777398,
		"in_reply_to_user_id_str" : "19777398",
		"in_reply_to_screen_name" : "FallonTonight",
		"user" : {
			"id" : 19777398,
			"id_str" : "19777398",
			"name" : "The Tonight Show",
			"screen_name" : "FallonTonight",
			"location" : "Currently at Jimmy's home.",
			"description" : "The Tonight Show starring @JimmyFallon\nWeeknights 11:35/10:35c on @NBC\nTweet along with us using #FallonTonight",
			"url" : "http://t.co/fgp5RYqr3T",
			"entities" : {
				"url" : {
					"urls" : [
						{
							"url" : "http://t.co/fgp5RYqr3T",
							"expanded_url" : "http://www.tonightshow.com",
							"display_url" : "tonightshow.com",
							"indices" : [
								0,
								22
							]
						}
					]
				},
				"description" : {
					"urls" : [ ]
				}
			},
			"protected" : False,
			"followers_count" : 4206692,
			"friends_count" : 21559,
			"listed_count" : 10880,
			"created_at" : "Fri Jan 30 17:26:46 +0000 2009",
			"favourites_count" : 132023,
			"utc_offset" : None,
			"time_zone" : None,
			"geo_enabled" : True,
			"verified" : True,
			"statuses_count" : 83393,
			"lang" : None,
			"contributors_enabled" : False,
			"is_translator" : False,
			"is_translation_enabled" : False,
			"profile_background_color" : "03253E",
			"profile_background_image_url" : "http://abs.twimg.com/images/themes/theme1/bg.png",
			"profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme1/bg.png",
			"profile_background_tile" : False,
			"profile_image_url" : "http://pbs.twimg.com/profile_images/1232397389467615239/WRBCmphp_normal.jpg",
			"profile_image_url_https" : "https://pbs.twimg.com/profile_images/1232397389467615239/WRBCmphp_normal.jpg",
			"profile_banner_url" : "https://pbs.twimg.com/profile_banners/19777398/1536081506",
			"profile_link_color" : "0084B4",
			"profile_sidebar_border_color" : "FFFFFF",
			"profile_sidebar_fill_color" : "DDFFCC",
			"profile_text_color" : "333333",
			"profile_use_background_image" : True,
			"has_extended_profile" : False,
			"default_profile" : False,
			"default_profile_image" : False,
			"following" : False,
			"follow_request_sent" : False,
			"notifications" : False,
			"translator_type" : "none"
		},
		"geo" : None,
		"coordinates" : None,
		"place" : None,
		"contributors" : None,
		"is_quote_status" : False,
		"retweet_count" : 32,
		"favorite_count" : 299,
		"favorited" : False,
		"retweeted" : False,
		"lang" : "en"
	},
	"retweet_count" : 173,
	"favorite_count" : 1719,
	"favorited" : False,
	"retweeted" : False,
	"possibly_sensitive" : False,
	"lang" : "en"
}

cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})

# Finally, to check for retweets
tweet = {
	"created_at" : "Fri Apr 17 03:59:58 +0000 2020",
	"id" : 1250997404641476609,
	"id_str" : "1250997404641476609",
	"text" : "RT @WNBA: Party with us at home. \n\nAfter watching the #WNBADraft 2020 on @espn, join us on Instagram LIVE at 9pm/et for the afterparty! 🎉 h…",
	"truncated" : False,
	"entities" : {
		"hashtags" : [
			{
				"text" : "WNBADraft",
				"indices" : [
					54,
					64
				]
			}
		],
		"symbols" : [ ],
		"user_mentions" : [
			{
				"screen_name" : "WNBA",
				"name" : "WNBA",
				"id" : 17159397,
				"id_str" : "17159397",
				"indices" : [
					3,
					8
				]
			},
			{
				"screen_name" : "espn",
				"name" : "ESPN",
				"id" : 2557521,
				"id_str" : "2557521",
				"indices" : [
					73,
					78
				]
			}
		],
		"urls" : [ ]
	},
	"source" : "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id" : None,
	"in_reply_to_status_id_str" : None,
	"in_reply_to_user_id" : None,
	"in_reply_to_user_id_str" : None,
	"in_reply_to_screen_name" : None,
	"user" : 19923144,
	"geo" : None,
	"coordinates" : None,
	"place" : None,
	"contributors" : None,
	"retweeted_status" : {
		"created_at" : "Fri Apr 17 03:59:00 +0000 2020",
		"id" : 1250997160977580033,
		"id_str" : "1250997160977580033",
		"text" : "Party with us at home. \n\nAfter watching the #WNBADraft 2020 on @espn, join us on Instagram LIVE at 9pm/et for the a… https://t.co/fuK8eh8lF9",
		"truncated" : True,
		"entities" : {
			"hashtags" : [
				{
					"text" : "WNBADraft",
					"indices" : [
						44,
						54
					]
				}
			],
			"symbols" : [ ],
			"user_mentions" : [
				{
					"screen_name" : "espn",
					"name" : "ESPN",
					"id" : 2557521,
					"id_str" : "2557521",
					"indices" : [
						63,
						68
					]
				}
			],
			"urls" : [
				{
					"url" : "https://t.co/fuK8eh8lF9",
					"expanded_url" : "https://twitter.com/i/web/status/1250997160977580033",
					"display_url" : "twitter.com/i/web/status/1…",
					"indices" : [
						117,
						140
					]
				}
			]
		},
		"source" : "<a href=\"https://studio.twitter.com\" rel=\"nofollow\">Twitter Media Studio</a>",
		"in_reply_to_status_id" : None,
		"in_reply_to_status_id_str" : None,
		"in_reply_to_user_id" : None,
		"in_reply_to_user_id_str" : None,
		"in_reply_to_screen_name" : None,
		"user" : {
			"id" : 17159397,
			"id_str" : "17159397",
			"name" : "WNBA",
			"screen_name" : "WNBA",
			"location" : "",
			"description" : "The official Twitter account of the #WNBA #WNBADraft 2020: Friday, April 17 at 7 pm/et on ESPN!",
			"url" : "https://t.co/mNt0UYF0Aa",
			"entities" : {
				"url" : {
					"urls" : [
						{
							"url" : "https://t.co/mNt0UYF0Aa",
							"expanded_url" : "http://WNBA.com",
							"display_url" : "WNBA.com",
							"indices" : [
								0,
								23
							]
						}
					]
				},
				"description" : {
					"urls" : [ ]
				}
			},
			"protected" : False,
			"followers_count" : 616531,
			"friends_count" : 2105,
			"listed_count" : 2881,
			"created_at" : "Tue Nov 04 16:04:48 +0000 2008",
			"favourites_count" : 6198,
			"utc_offset" : None,
			"time_zone" : None,
			"geo_enabled" : True,
			"verified" : True,
			"statuses_count" : 70358,
			"lang" : None,
			"contributors_enabled" : False,
			"is_translator" : False,
			"is_translation_enabled" : False,
			"profile_background_color" : "FFFFFF",
			"profile_background_image_url" : "http://abs.twimg.com/images/themes/theme1/bg.png",
			"profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme1/bg.png",
			"profile_background_tile" : False,
			"profile_image_url" : "http://pbs.twimg.com/profile_images/1145670653145735168/KPFFWIZZ_normal.jpg",
			"profile_image_url_https" : "https://pbs.twimg.com/profile_images/1145670653145735168/KPFFWIZZ_normal.jpg",
			"profile_banner_url" : "https://pbs.twimg.com/profile_banners/17159397/1586785583",
			"profile_link_color" : "FF0000",
			"profile_sidebar_border_color" : "000000",
			"profile_sidebar_fill_color" : "FFF7CC",
			"profile_text_color" : "0C3E53",
			"profile_use_background_image" : True,
			"has_extended_profile" : False,
			"default_profile" : False,
			"default_profile_image" : False,
			"following" : False,
			"follow_request_sent" : False,
			"notifications" : False,
			"translator_type" : "none"
		},
		"geo" : None,
		"coordinates" : None,
		"place" : None,
		"contributors" : None,
		"is_quote_status" : False,
		"retweet_count" : 23,
		"favorite_count" : 115,
		"favorited" : False,
		"retweeted" : False,
		"possibly_sensitive" : False,
		"lang" : "en"
	},
	"is_quote_status" : False,
	"retweet_count" : 23,
	"favorite_count" : 0,
	"favorited" : False,
	"retweeted" : False,
	"lang" : "en"
}

cc.save_tweet({
	"bot_id": 31868,
	"data": tweet
})

cc.close()