from wrappers.postgresql_wrapper import PostgresAPI
import api.signal

p = PostgresAPI()


#print(p.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 100, "retweets": 2}))

print(p.insert_log({"bot_id": 1244051405721255937, "action": "SAVING TWEET224 (1244051405721255937)","target_id" : 25365536}))



print(p.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 1012124120, "retweets": 2}))

