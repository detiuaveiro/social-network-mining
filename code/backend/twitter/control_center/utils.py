import re


def tweet_to_simple_text(tweet: str) -> str:
	return re.sub(r'@.*? | \n | http.* | #.*?', '', tweet).encode('latin-1', 'ignore').decode('latin-1')
