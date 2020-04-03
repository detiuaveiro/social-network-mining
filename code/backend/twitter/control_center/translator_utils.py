from googletrans import Translator as Google_translator


class Translator(Google_translator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_pt_to_en(self, text):
        return self.translate(text, src='pt', dest='en').text

    def from_en_to_pt(self, text):
        return self.translate(text, src='en', dest='pt').text

    def from_any_to_pt(self, text):
        return self.translate(text, dest='pt').text
