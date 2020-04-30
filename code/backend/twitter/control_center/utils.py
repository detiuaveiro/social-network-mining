import re


def tweet_to_simple_text(tweet: str) -> str:
	text_with_emojis = re.sub(r'@.*? |\n|http.*', '', tweet).encode('ascii', 'ignore').decode('ascii')
	return text_with_emojis.encode('latin-1', 'ignore').decode('latin-1')
