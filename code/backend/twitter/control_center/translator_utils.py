import logging
from googletrans import Translator as Google_translator
import pydeepl


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
			return pydeepl.translate(text, from_lang='pt', to_lang='en')
		except Exception as error:
			log.exception(f"Error <{error}> translating text <{text}> from portuguese to english: ")
			return None

	def from_en_to_pt(self, text):
		try:
			return pydeepl.translate(text, from_lang='en', to_lang='pt').text
		except Exception as error:
			log.exception(f"Error <{error}> translating text <{text}> from english to portuguese: ")
			return None
