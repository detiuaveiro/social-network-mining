import re
import zmq
import json
import logging
from enum import IntEnum

import nltk.chat.eliza as eliza
import nltk.chat.rude as rude
import nltk.chat.suntsu as suntsu
import nltk.chat.zen as zen

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


logger = logging.getLogger("text-generator")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("text_generator.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


def tweet_to_simple_text(tweet: str) -> str:
	return re.sub(r'@.*? |\n|http.*', '', tweet).encode('ascii', 'ignore').decode('ascii')


class DumbReplier:
	"""Dumb replier implemented using Eliza bot style
	"""

	class DumbReplierTypes(IntEnum):
		ELIZA_REPLIER = 0
		RUDE_REPLIER = 1
		SUNTZU_REPLIER = 2
		ZEN_REPLIER = 3

	def __init__(self, replier_type: DumbReplierTypes = None):
		"""The default replier is an Eliza style bot
		"""
		self.bot = eliza.eliza_chatbot

		if replier_type == DumbReplier.DumbReplierTypes.RUDE_REPLIER:
			self.bot = rude.rude_chatbot
		elif replier_type == DumbReplier.DumbReplierTypes.SUNTZU_REPLIER:
			self.bot = suntsu.suntsu_chatbot
		elif replier_type == DumbReplier.DumbReplierTypes.ZEN_REPLIER:
			self.bot = zen.zen_chatbot

	def generate_response(self, text: str) -> str:
		return self.bot.respond(text)


class SmarterReplier:
	"""Slightly smarter replier than the dumber, but still dumb
	"""

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


class ParlaiReplier:
	"""Smartest of the repliers, in which we send an request to a parlai server running on our machines
	"""

	def __init__(self, host, port):
		self.socket = zmq.Context().socket(zmq.REQ)
		self.socket.setsockopt(zmq.LINGER, 1)
		self.host = f"tcp://{host}:{port}"

	def generate_response(self, text: str) -> str:
		logger.info(f"Starting to get a response from ParlAI server for the text: {text}")

		message = {
			'id': 'bot',
			'text': text,
			# 'label_candidates': ['quarantine', 'government',  'diseases'],
			'episode_done': False,
		}

		try:
			self.socket.connect(self.host)
			self.socket.send_unicode(json.dumps(message))
			reply = json.loads(self.socket.recv_unicode())
			self.socket.close()

			logger.info(f"Got response <{reply}> form ParlAI for the text <{text}>")

			return reply['text']
		except Exception as error:
			logger.exception(f"Error <{error}> when trying to obtain a response to the text <{text}>: ")
			return None


def test_smarter_replier():
	replier = SmarterReplier()

	while True:
		print(replier.generate_response(input("> ")))


if __name__ == "__main__":
	test_smarter_replier()
