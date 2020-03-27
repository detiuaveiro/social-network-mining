from translator_utils import Translator
import nltk.chat.eliza as eliza
import nltk.chat.rude as rude
import nltk.chat.suntsu as suntsu
import nltk.chat.zen as zen


def main():
	translator = Translator()
	bot = eliza.eliza_chatbot
	bot2 = rude.rude_chatbot
	bot3 = suntsu.suntsu_chatbot
	bot4 = zen.zen_chatbot

	while True:
		answer_en = bot4.respond(translator.from_pt_to_en(input("> ")))
		print(translator.from_en_to_pt(answer_en))


if __name__ == "__main__":
	main()
