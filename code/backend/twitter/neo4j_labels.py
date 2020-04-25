# Labels for Nodes and Relationships
BOT_LABEL = "Bot"
USER_LABEL = "User"
TWEET_LABEL = "Tweet"
WROTE_LABEL = "WROTE"
RETWEET_LABEL = "RETWEETED"
QUOTE_LABEL = "QUOTED"
REPLY_LABEL = "REPLIED"
FOLLOW_LABEL = "FOLLOWS"
QUERY = "match (b:Bot) - [r] - (t:Tweet) - [r2] - (t2:Tweet)" \
		"call apoc.cypher.run('with `t` as t match (u:User) -[]-(t) return u, t limit 50', {t:t})" \
		"Yield value"\
		"return b, value.u, t, r2, t2" \
		"limit 150"
