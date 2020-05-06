import re


def tweet_to_simple_text(tweet: str) -> str:
	return " ".join(
		re.sub(r'@.*?[\n\s]+|\n|http.*|RT.*?: ', '', tweet).encode('latin-1', 'ignore').decode('latin-1').split())
