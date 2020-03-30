from control_center.PDP import PDP

if __name__ == '__main__':
	pdp = PDP()
	req = {
		"bot_id":1103294806497902594,
		"user_id": 19923144,
		"tweet_id": 1130717914905096192,
		"tweet_text": "RT @nbastats: HISTORY!\n\nSteph Curry and Draymond Green become the first teammates in @NBAHistory to both record a triple-double in the same…",
		"tweet_entities": {
			"hashtags" : [ ],
			"symbols" : [ ],
			"user_mentions" : [
				{
					"screen_name" : "nbastats",
					"name" : "NBA.com/Stats",
					"id" : 283090686,
					"id_str" : "283090686",
					"indices" : [
						3,
						12
					]
				},
				{
					"screen_name" : "NBAHistory",
					"name" : "NBA History",
					"id" : 171165627,
					"id_str" : "171165627",
					"indices" : [
						85,
						96
					]
				}
			],
			"urls" : [ ]
		},
	}

	for policy in pdp.postgres.search_policies()["data"]:
		pdp._bot_is_targeted(policy, req)
