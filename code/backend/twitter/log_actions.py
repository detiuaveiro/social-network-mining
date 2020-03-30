# -----------------------------------------------------------
# PostgreSQL Log table Actions
# -----------------------------------------------------------

RETWEET = "RETWEET" 															#target: tweet ID
FOLLOW = "FOLLOW" 																#target: user id
TWEET_LIKE = "TWEET LIKE"														#target: tweet ID
TWEET_REPLY = "TWEET REPLY" 													#target: tweet reply ID
LIKE_REQ = "REQUEST LIKE" 														#target: tweet ID
LIKE_REQ_ACCEPT = "REQUEST LIKE ACCEPTED" 										#target: tweet ID
LIKE_REQ_DENY = "REQUEST LIKE DENIED" 											#target: tweet ID
RETWEET_REQ = "REQUEST RETWEET" 												#target: tweet ID
RETWEET_REQ_ACCEPT = "REQUEST RETWEET ACCEPTED" 								#target: tweet ID
RETWEET_REQ_DENY = "REQUEST RETWEET DENIED" 									#target: tweet ID
REPLY_REQ = "REQUEST REPLY" 													#target: tweet ID
REPLY_REQ_ACCEPT = "REQUEST REPLY ACCEPTED" 									#target: tweet ID
REPLY_REQ_DENY = "REQUEST REPLY DENIED"											#target: tweet ID
FOLLOW_REQ = "REQUEST FOLLOW" 													#target: user ID
FOLLOW_REQ_ACCEPT = "REQUEST FOLLOW ACCEPTED" 									#target: user ID
FOLLOW_REQ_DENY = "REQUEST FOLLOW DENIED" 										#target: user ID
UPDATE_USER = "UPDATE USER" 													#target: user ID
INSERT_USER = "INSERT USER" 													#target: user ID
UPDATE_TWEET = "UPDATE TWEET" 													#target: tweet ID
INSERT_TWEET = "INSERT TWEET" 													#target: tweet ID
UPDATE_MESSAGE = "UPDATE MESSAGE" 												#target: message ID
INSERT_MESSAGE = "INSERT MESSAGE" 												#target: message ID
ERROR = "ERROR"