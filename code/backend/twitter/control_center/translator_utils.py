import logging
from googletrans import Translator as Google_translator


log = logging.getLogger('Translator')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("translator.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class Translator(Google_translator):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def from_pt_to_en(self, text):
		try:
			return self.translate(text, src='pt', dest='en').text
		except Exception as error:
			log.exception(f"Error <{error}> translating text <{text}> from portuguese to english: ")
			return None

	def from_en_to_pt(self, text):
		try:
			return self.translate(text, src='en', dest='pt').text
		except Exception as error:
			log.exception(f"Error <{error}> translating text <{text}> from english to portuguese: ")
			return None
