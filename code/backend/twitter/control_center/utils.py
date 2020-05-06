import re


def tweet_to_simple_text(tweet: str) -> str:
	return " ".join(re.sub(r'@.*?[\n\s]+|\n|http.*|#.*?[\n\s]+|RT.*?: ', '',
	                       f"{tweet}\n").encode('latin-1', 'ignore').decode('latin-1').split())
