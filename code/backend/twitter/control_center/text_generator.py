import re
from enum import IntEnum

import nltk.chat.eliza as eliza
import nltk.chat.rude as rude
import nltk.chat.suntsu as suntsu
import nltk.chat.zen as zen

from control_center.translator_utils import Translator

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer


def tweet_to_simple_text(tweet: str) -> str:
	return re.sub(r'@.*? |\n|http.*', '', tweet).encode('ascii', 'ignore').decode('ascii')


class DumbReplierTypes(IntEnum):
	ELIZA_REPLIER = 0
	RUDE_REPLIER = 1
	SUNTZU_REPLIER = 2
	ZEN_REPLIER = 3


class DumbReplier:
	def __init__(self, replier_type: DumbReplierTypes = None):
		"""The default replier is an Eliza style bot
		"""
		self.translator = Translator()
		self.bot = eliza.eliza_chatbot

		if replier_type == DumbReplierTypes.RUDE_REPLIER:
			self.bot = rude.rude_chatbot
		elif replier_type == DumbReplierTypes.SUNTZU_REPLIER:
			self.bot = suntsu.suntsu_chatbot
		elif replier_type == DumbReplierTypes.ZEN_REPLIER:
			self.bot = zen.zen_chatbot

	def generate_response(self, text: str) -> str:
		response_en = self.bot.respond(self.translator.from_pt_to_en(text))
		return self.translator.from_en_to_pt(response_en)


class SmarterReplier:
	def __init__(self):
		self.bot = ChatBot("Me very smart")
		self.trainer = ChatterBotCorpusTrainer(self.bot) # ListTrainer(self.bot)

		# with open("control_center/data/PS/antoniocostapm_tweets.csv", 'r') as file:
		# 	self.trainer.train(file.readlines())

		self.trainer.train("chatterbot.corpus.portuguese")

	def generate_response(self, text: str) -> str:
		response = self.bot.get_response(text)
		print(response.confidence)
		return response


def test():
	replier = SmarterReplier()

	while True:
		print(replier.generate_response(input("> ")))


if __name__ == "__main__":
	test()
