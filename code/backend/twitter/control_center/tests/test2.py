from control_center.control_center import Control_Center

cc = Control_Center()

to_send = {
	"bot_id": 31868,
	"bot_name": "fag",
	"bot_screen_name": "FagGoT",
	"data": None
}

# First we must test that it's inserting tweets on neo4j when everything's normal
tweet = {
	"id": 781211078550102016,
	"id_str": "781211078550102016",
	"full_text": "My friend needed sweatpants in order to go in her lab and take a quiz so I'm just chilling in the"
	             " restroom for 50 mins with booty shorts on https://t.co/cbWCeYa5wF",
	"truncated": False,
	"display_text_range": [
		0,
		139
	],
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [],
		"urls": [],
		"media": [
			{
				"id": 781211062397833216,
				"id_str": "781211062397833216",
				"indices": [
					140,
					163
				],
				"media_url": "http://pbs.twimg.com/media/CtdrUnzUEAAB1MA.jpg",
				"media_url_https": "https://pbs.twimg.com/media/CtdrUnzUEAAB1MA.jpg",
				"url": "https://t.co/cbWCeYa5wF",
				"display_url": "pic.twitter.com/cbWCeYa5wF",
				"expanded_url": "https://twitter.com/Anguyenballer/status/781211078550102016/photo/1",
				"type": "photo",
				"sizes": {
					"thumb": {
						"w": 150,
						"h": 150,
						"resize": "crop"
					},
					"large": {
						"w": 1536,
						"h": 2048,
						"resize": "fit"
					},
					"small": {
						"w": 510,
						"h": 680,
						"resize": "fit"
					},
					"medium": {
						"w": 900,
						"h": 1200,
						"resize": "fit"
					}
				}
			}
		]
	},
	"extended_entities": {
		"media": [
			{
				"id": 781211062397833216,
				"id_str": "781211062397833216",
				"indices": [
					140,
					163
				],
				"media_url": "http://pbs.twimg.com/media/CtdrUnzUEAAB1MA.jpg",
				"media_url_https": "https://pbs.twimg.com/media/CtdrUnzUEAAB1MA.jpg",
				"url": "https://t.co/cbWCeYa5wF",
				"display_url": "pic.twitter.com/cbWCeYa5wF",
				"expanded_url": "https://twitter.com/Anguyenballer/status/781211078550102016/photo/1",
				"type": "photo",
				"sizes": {
					"thumb": {
						"w": 150,
						"h": 150,
						"resize": "crop"
					},
					"large": {
						"w": 1536,
						"h": 2048,
						"resize": "fit"
					},
					"small": {
						"w": 510,
						"h": 680,
						"resize": "fit"
					},
					"medium": {
						"w": 900,
						"h": 1200,
						"resize": "fit"
					}
				}
			}
		]
	},
	"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id": None,
	"in_reply_to_status_id_str": None,
	"in_reply_to_user_id": None,
	"in_reply_to_user_id_str": None,
	"in_reply_to_screen_name": None,
	"user": {
		"id": 504751016,
		"id_str": "504751016",
		"name": "Nndrew Aguyen",
		"screen_name": "Anguyenballer",
		"location": "Arlington, TX",
		"description": "UTA’20 Nursing",
		"url": "https://t.co/CTOTumnm3Y",
		"entities": {
			"url": {
				"urls": [
					{
						"url": "https://t.co/CTOTumnm3Y",
						"expanded_url": "https://www.instagram.com/andrewnguyen03/",
						"display_url": "instagram.com/andrewnguyen03/",
						"indices": [
							0,
							23
						]
					}
				]
			},
			"description": {
				"urls": []
			}
		},
		"protected": False,
		"followers_count": 4754,
		"friends_count": 1093,
		"listed_count": 78,
		"created_at": "Sun Feb 26 17:05:40 +0000 2012",
		"favourites_count": 12686,
		"utc_offset": None,
		"time_zone": None,
		"geo_enabled": True,
		"verified": False,
		"statuses_count": 10452,
		"lang": None,
		"contributors_enabled": False,
		"is_translator": False,
		"is_translation_enabled": False,
		"profile_background_color": "C0DEED",
		"profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_tile": False,
		"profile_image_url": "http://pbs.twimg.com/profile_images/1255027503284043776/QE8gyoAz_normal.jpg",
		"profile_image_url_https": "https://pbs.twimg.com/profile_images/1255027503284043776/QE8gyoAz_normal.jpg",
		"profile_banner_url": "https://pbs.twimg.com/profile_banners/504751016/1583167218",
		"profile_link_color": "1DA1F2",
		"profile_sidebar_border_color": "C0DEED",
		"profile_sidebar_fill_color": "DDEEF6",
		"profile_text_color": "333333",
		"profile_use_background_image": True,
		"has_extended_profile": True,
		"default_profile": True,
		"default_profile_image": False,
		"following": False,
		"follow_request_sent": False,
		"notifications": False,
		"translator_type": "none"
	},
	"geo": None,
	"coordinates": None,
	"place": None,
	"contributors": None,
	"is_quote_status": False,
	"retweet_count": 127838,
	"favorite_count": 352853,
	"favorited": False,
	"retweeted": False,
	"possibly_sensitive": False,
	"lang": "en"
}

to_send['data'] = tweet
cc.save_tweet(to_send)

# Check if replying creates both nodes
tweet = {
	"id": 1242941557126434816,
	"id_str": "1242941557126434816",
	"full_text": "@koalitahtururu É cada uma",
	"truncated": False,
	"display_text_range": [
		16,
		26
	],
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [
			{
				"screen_name": "koalitahtururu",
				"name": "V",
				"id": 978976914584064000,
				"id_str": "978976914584064000",
				"indices": [
					0,
					15
				]
			}
		],
		"urls": []
	},
	"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
	"in_reply_to_status_id": 1242936564537266176,
	"in_reply_to_status_id_str": "1242936564537266176",
	"in_reply_to_user_id": 978976914584064000,
	"in_reply_to_user_id_str": "978976914584064000",
	"in_reply_to_screen_name": "koalitahtururu",
	"user": {
		"id": 783417520350978048,
		"id_str": "783417520350978048",
		"name": "Tiago Oliveira",
		"screen_name": "nyclide",
		"location": "Lisboa",
		"description": "🎥 Videographer | 📷 Photographer | 🇵🇹 JCH",
		"url": None,
		"entities": {
			"description": {
				"urls": []
			}
		},
		"protected": False,
		"followers_count": 99,
		"friends_count": 60,
		"listed_count": 0,
		"created_at": "Tue Oct 04 21:24:27 +0000 2016",
		"favourites_count": 873,
		"utc_offset": None,
		"time_zone": None,
		"geo_enabled": False,
		"verified": False,
		"statuses_count": 954,
		"lang": None,
		"contributors_enabled": False,
		"is_translator": False,
		"is_translation_enabled": False,
		"profile_background_color": "F5F8FA",
		"profile_background_image_url": None,
		"profile_background_image_url_https": None,
		"profile_background_tile": False,
		"profile_image_url": "http://pbs.twimg.com/profile_images/1224447903629893633/yqqjNvVr_normal.jpg",
		"profile_image_url_https": "https://pbs.twimg.com/profile_images/1224447903629893633/yqqjNvVr_normal.jpg",
		"profile_banner_url": "https://pbs.twimg.com/profile_banners/783417520350978048/1580766137",
		"profile_link_color": "1DA1F2",
		"profile_sidebar_border_color": "C0DEED",
		"profile_sidebar_fill_color": "DDEEF6",
		"profile_text_color": "333333",
		"profile_use_background_image": True,
		"has_extended_profile": False,
		"default_profile": True,
		"default_profile_image": False,
		"following": False,
		"follow_request_sent": False,
		"notifications": False,
		"translator_type": "none"
	},
	"geo": None,
	"coordinates": None,
	"place": None,
	"contributors": None,
	"is_quote_status": False,
	"retweet_count": 0,
	"favorite_count": 0,
	"favorited": False,
	"retweeted": False,
	"lang": "pt"
}

to_send['data'] = tweet
cc.save_tweet(to_send)

# Check if quoting creates both nodes
tweet = {
	"id": 1242817359980703746,
	"id_str": "1242817359980703746",
	"full_text": "RT @vpcrlhpfv2: Isso não é verdade, no meu ponto de vista quem desiste é quem está farto de tentar e "
	             "vê que já não há volta a dar",
	"truncated": False,
	"display_text_range": [
		0,
		129
	],
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [
			{
				"screen_name": "vpcrlhpfv2",
				"name": "Francisco🇨🇴",
				"id": 1225413999526895616,
				"id_str": "1225413999526895616",
				"indices": [
					3,
					14
				]
			}
		],
		"urls": []
	},
	"source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
	"in_reply_to_status_id": None,
	"in_reply_to_status_id_str": None,
	"in_reply_to_user_id": None,
	"in_reply_to_user_id_str": None,
	"in_reply_to_screen_name": None,
	"user": {
		"id": 2266400298,
		"id_str": "2266400298",
		"name": "MotoRato",
		"screen_name": "Bezugodelado",
		"location": "Lisboa",
		"description": "Sou um gajo assim pó estranho.. não liguem.\n\nVarzim eSports🎮\nFutsal ⚽",
		"url": None,
		"entities": {
			"description": {
				"urls": []
			}
		},
		"protected": False,
		"followers_count": 178,
		"friends_count": 143,
		"listed_count": 1,
		"created_at": "Sat Dec 28 20:27:37 +0000 2013",
		"favourites_count": 2234,
		"utc_offset": None,
		"time_zone": None,
		"geo_enabled": True,
		"verified": False,
		"statuses_count": 5525,
		"lang": None,
		"contributors_enabled": False,
		"is_translator": False,
		"is_translation_enabled": False,
		"profile_background_color": "C0DEED",
		"profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_tile": False,
		"profile_image_url": "http://pbs.twimg.com/profile_images/1242018809373958149/x2Jhuhzu_normal.jpg",
		"profile_image_url_https": "https://pbs.twimg.com/profile_images/1242018809373958149/x2Jhuhzu_normal.jpg",
		"profile_banner_url": "https://pbs.twimg.com/profile_banners/2266400298/1584955335",
		"profile_link_color": "FCFC08",
		"profile_sidebar_border_color": "C0DEED",
		"profile_sidebar_fill_color": "DDEEF6",
		"profile_text_color": "333333",
		"profile_use_background_image": True,
		"has_extended_profile": False,
		"default_profile": False,
		"default_profile_image": False,
		"following": False,
		"follow_request_sent": False,
		"notifications": False,
		"translator_type": "none"
	},
	"geo": None,
	"coordinates": None,
	"place": None,
	"contributors": None,
	"retweeted_status": {
		"created_at": "Tue Mar 24 00:30:40 +0000 2020",
		"id": 1242247422564347904,
		"id_str": "1242247422564347904",
		"full_text": "Isso não é verdade, no meu ponto de vista quem desiste é quem está farto de tentar e vê que já não "
		             "há volta a dar https://t.co/trJyWeZc3K",
		"truncated": False,
		"display_text_range": [
			0,
			113
		],
		"entities": {
			"hashtags": [],
			"symbols": [],
			"user_mentions": [],
			"urls": [
				{
					"url": "https://t.co/trJyWeZc3K",
					"expanded_url": "https://twitter.com/palagoinha/status/1241936063561699330",
					"display_url": "twitter.com/palagoinha/sta…",
					"indices": [
						114,
						137
					]
				}
			]
		},
		"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
		"in_reply_to_status_id": None,
		"in_reply_to_status_id_str": None,
		"in_reply_to_user_id": None,
		"in_reply_to_user_id_str": None,
		"in_reply_to_screen_name": None,
		"user": {
			"id": 1225413999526895616,
			"id_str": "1225413999526895616",
			"name": "Francisco🇨🇴",
			"screen_name": "vpcrlhpfv2",
			"location": "2660",
			"description": "@SLBenfica // Ig: francisco.bojaca",
			"url": None,
			"entities": {
				"description": {
					"urls": []
				}
			},
			"protected": False,
			"followers_count": 4258,
			"friends_count": 568,
			"listed_count": 0,
			"created_at": "Thu Feb 06 13:40:52 +0000 2020",
			"favourites_count": 5335,
			"utc_offset": None,
			"time_zone": None,
			"geo_enabled": False,
			"verified": False,
			"statuses_count": 7304,
			"lang": None,
			"contributors_enabled": False,
			"is_translator": False,
			"is_translation_enabled": False,
			"profile_background_color": "F5F8FA",
			"profile_background_image_url": None,
			"profile_background_image_url_https": None,
			"profile_background_tile": False,
			"profile_image_url": "http://pbs.twimg.com/profile_images/1253629709348474881/i7y7GLhD_normal.jpg",
			"profile_image_url_https": "https://pbs.twimg.com/profile_images/1253629709348474881/i7y7GLhD_normal.jpg",
			"profile_banner_url": "https://pbs.twimg.com/profile_banners/1225413999526895616/1585852702",
			"profile_link_color": "1DA1F2",
			"profile_sidebar_border_color": "C0DEED",
			"profile_sidebar_fill_color": "DDEEF6",
			"profile_text_color": "333333",
			"profile_use_background_image": True,
			"has_extended_profile": True,
			"default_profile": True,
			"default_profile_image": False,
			"following": False,
			"follow_request_sent": False,
			"notifications": False,
			"translator_type": "none"
		},
		"geo": None,
		"coordinates": None,
		"place": None,
		"contributors": None,
		"is_quote_status": True,
		"quoted_status_id": 1241936063561699330,
		"quoted_status_id_str": "1241936063561699330",
		"quoted_status_permalink": {
			"url": "https://t.co/trJyWeZc3K",
			"expanded": "https://twitter.com/palagoinha/status/1241936063561699330",
			"display": "twitter.com/palagoinha/sta…"
		},
		"quoted_status": {
			"created_at": "Mon Mar 23 03:53:26 +0000 2020",
			"id": 1241936063561699330,
			"id_str": "1241936063561699330",
			"full_text": "Quem desiste, na verdade nunca quis.",
			"truncated": False,
			"display_text_range": [
				0,
				36
			],
			"entities": {
				"hashtags": [],
				"symbols": [],
				"user_mentions": [],
				"urls": []
			},
			"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
			"in_reply_to_status_id": None,
			"in_reply_to_status_id_str": None,
			"in_reply_to_user_id": None,
			"in_reply_to_user_id_str": None,
			"in_reply_to_screen_name": None,
			"user": {
				"id": 792843051387478017,
				"id_str": "792843051387478017",
				"name": "alagoinha",
				"screen_name": "palagoinha",
				"location": "",
				"description": "ig: pedroalagoinha",
				"url": "https://t.co/Kd3sPj6y2K",
				"entities": {
					"url": {
						"urls": [
							{
								"url": "https://t.co/Kd3sPj6y2K",
								"expanded_url": "http://curiouscat.me/alagoinha",
								"display_url": "curiouscat.me/alagoinha",
								"indices": [
									0,
									23
								]
							}
						]
					},
					"description": {
						"urls": []
					}
				},
				"protected": False,
				"followers_count": 6952,
				"friends_count": 2519,
				"listed_count": 3,
				"created_at": "Sun Oct 30 21:38:08 +0000 2016",
				"favourites_count": 15325,
				"utc_offset": None,
				"time_zone": None,
				"geo_enabled": True,
				"verified": False,
				"statuses_count": 16637,
				"lang": None,
				"contributors_enabled": False,
				"is_translator": False,
				"is_translation_enabled": False,
				"profile_background_color": "000000",
				"profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
				"profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
				"profile_background_tile": False,
				"profile_image_url": "http://pbs.twimg.com/profile_images/1251720319309615105/9uE8q1-m_normal.jpg",
				"profile_image_url_https": "https://pbs.twimg.com/profile_images/1251720319309615105/9uE8q1-m_normal.jpg",
				"profile_banner_url": "https://pbs.twimg.com/profile_banners/792843051387478017/1582677929",
				"profile_link_color": "FF691F",
				"profile_sidebar_border_color": "000000",
				"profile_sidebar_fill_color": "000000",
				"profile_text_color": "000000",
				"profile_use_background_image": False,
				"has_extended_profile": True,
				"default_profile": False,
				"default_profile_image": False,
				"following": False,
				"follow_request_sent": False,
				"notifications": False,
				"translator_type": "none"
			},
			"geo": None,
			"coordinates": None,
			"place": None,
			"contributors": None,
			"is_quote_status": False,
			"retweet_count": 2048,
			"favorite_count": 1586,
			"favorited": False,
			"retweeted": False,
			"lang": "pt"
		},
		"retweet_count": 1800,
		"favorite_count": 1640,
		"favorited": False,
		"retweeted": False,
		"possibly_sensitive": False,
		"lang": "pt"
	},
	"is_quote_status": True,
	"quoted_status_id": 1241936063561699330,
	"quoted_status_id_str": "1241936063561699330",
	"quoted_status_permalink": {
		"url": "https://t.co/trJyWeZc3K",
		"expanded": "https://twitter.com/palagoinha/status/1241936063561699330",
		"display": "twitter.com/palagoinha/sta…"
	},
	"retweet_count": 1800,
	"favorite_count": 0,
	"favorited": False,
	"retweeted": False,
	"lang": "pt"
}

to_send['data'] = tweet
cc.save_tweet(to_send)

# Finally, to check for retweets
tweet = {
	"id": 1255492799534858245,
	"id_str": "1255492799534858245",
	"full_text": "RT @nicolepf0: quarentena ta me a pôr a pensar demasiado nas cenas",
	"truncated": False,
	"display_text_range": [
		0,
		66
	],
	"entities": {
		"hashtags": [],
		"symbols": [],
		"user_mentions": [
			{
				"screen_name": "nicolepf0",
				"name": "nicole",
				"id": 1068927030643879938,
				"id_str": "1068927030643879938",
				"indices": [
					3,
					13
				]
			}
		],
		"urls": []
	},
	"source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
	"in_reply_to_status_id": None,
	"in_reply_to_status_id_str": None,
	"in_reply_to_user_id": None,
	"in_reply_to_user_id_str": None,
	"in_reply_to_screen_name": None,
	"user": {
		"id": 3347056546,
		"id_str": "3347056546",
		"name": "Mariana",
		"screen_name": "marianabarbas",
		"location": "Rossão",
		"description": "19y\nAlmada 📍\nIPG| GRH 🎓",
		"url": None,
		"entities": {
			"description": {
				"urls": []
			}
		},
		"protected": False,
		"followers_count": 133,
		"friends_count": 107,
		"listed_count": 0,
		"created_at": "Fri Jun 26 22:35:32 +0000 2015",
		"favourites_count": 2625,
		"utc_offset": None,
		"time_zone": None,
		"geo_enabled": True,
		"verified": False,
		"statuses_count": 10112,
		"lang": None,
		"contributors_enabled": False,
		"is_translator": False,
		"is_translation_enabled": False,
		"profile_background_color": "000000",
		"profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
		"profile_background_tile": False,
		"profile_image_url": "http://pbs.twimg.com/profile_images/1120698688144326656/qehQmCWF_normal.jpg",
		"profile_image_url_https": "https://pbs.twimg.com/profile_images/1120698688144326656/qehQmCWF_normal.jpg",
		"profile_banner_url": "https://pbs.twimg.com/profile_banners/3347056546/1528912609",
		"profile_link_color": "FF691F",
		"profile_sidebar_border_color": "000000",
		"profile_sidebar_fill_color": "000000",
		"profile_text_color": "000000",
		"profile_use_background_image": False,
		"has_extended_profile": True,
		"default_profile": False,
		"default_profile_image": False,
		"following": False,
		"follow_request_sent": False,
		"notifications": False,
		"translator_type": "none"
	},
	"geo": None,
	"coordinates": None,
	"place": None,
	"contributors": None,
	"retweeted_status": {
		"created_at": "Sun Apr 26 00:51:05 +0000 2020",
		"id": 1254211361963413509,
		"id_str": "1254211361963413509",
		"full_text": "quarentena ta me a pôr a pensar demasiado nas cenas",
		"truncated": False,
		"display_text_range": [
			0,
			51
		],
		"entities": {
			"hashtags": [],
			"symbols": [],
			"user_mentions": [],
			"urls": []
		},
		"source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
		"in_reply_to_status_id": None,
		"in_reply_to_status_id_str": None,
		"in_reply_to_user_id": None,
		"in_reply_to_user_id_str": None,
		"in_reply_to_screen_name": None,
		"user": {
			"id": 1068927030643879938,
			"id_str": "1068927030643879938",
			"name": "nicole",
			"screen_name": "nicolepf0",
			"location": "Torres Vedras, Portugal",
			"description": "Don't rush, slow touch.. \n     \n		      \n						       Ig: _nicolepferreira",
			"url": None,
			"entities": {
				"description": {
					"urls": []
				}
			},
			"protected": False,
			"followers_count": 562,
			"friends_count": 159,
			"listed_count": 0,
			"created_at": "Sat Dec 01 17:57:18 +0000 2018",
			"favourites_count": 7110,
			"utc_offset": None,
			"time_zone": None,
			"geo_enabled": False,
			"verified": False,
			"statuses_count": 5701,
			"lang": None,
			"contributors_enabled": False,
			"is_translator": False,
			"is_translation_enabled": False,
			"profile_background_color": "F5F8FA",
			"profile_background_image_url": None,
			"profile_background_image_url_https": None,
			"profile_background_tile": False,
			"profile_image_url": "http://pbs.twimg.com/profile_images/1251495712824623110/lNQcalpr_normal.jpg",
			"profile_image_url_https": "https://pbs.twimg.com/profile_images/1251495712824623110/lNQcalpr_normal.jpg",
			"profile_banner_url": "https://pbs.twimg.com/profile_banners/1068927030643879938/1583193436",
			"profile_link_color": "1DA1F2",
			"profile_sidebar_border_color": "C0DEED",
			"profile_sidebar_fill_color": "DDEEF6",
			"profile_text_color": "333333",
			"profile_use_background_image": True,
			"has_extended_profile": True,
			"default_profile": True,
			"default_profile_image": False,
			"following": False,
			"follow_request_sent": False,
			"notifications": False,
			"translator_type": "none"
		},
		"geo": None,
		"coordinates": None,
		"place": None,
		"contributors": None,
		"is_quote_status": False,
		"retweet_count": 3910,
		"favorite_count": 2486,
		"favorited": True,
		"retweeted": True,
		"lang": "pt"
	},
	"is_quote_status": False,
	"retweet_count": 3910,
	"favorite_count": 0,
	"favorited": True,
	"retweeted": True,
	"lang": "pt"
}

to_send['data'] = tweet
cc.save_tweet(to_send)

cc.close()
