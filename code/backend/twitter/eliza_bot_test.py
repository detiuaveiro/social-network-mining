import re

from control_center.translator_utils import Translator
from wrappers.mongo_wrapper import MongoAPI

import nltk.chat.eliza as eliza
import nltk.chat.rude as rude
import nltk.chat.suntsu as suntsu
import nltk.chat.zen as zen


def tweet_to_simple_text(tweet: str) -> str:
	return re.sub(r'@.*? |\n|http.*', '', tweet).encode('ascii', 'ignore').decode('ascii')


def main():
	mongo = MongoAPI()
	tweets_pt = [tweet['text'] for tweet in mongo.search(collection="tweets", query={"lang": "pt"}, fields=["text"])]

	translator = Translator()
	bot = eliza.eliza_chatbot
	bot2 = rude.rude_chatbot
	bot3 = suntsu.suntsu_chatbot
	bot4 = zen.zen_chatbot

	for tweet in [tweet_to_simple_text(tweet) for tweet in list(set(tweets_pt))]:
		print(f"> {tweet}")
		answer_en = bot.respond(translator.from_pt_to_en(tweet))
		print(translator.from_en_to_pt(answer_en))


if __name__ == "__main__":
	main()
