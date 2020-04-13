import sys
import spacy_udpipe

spacy_udpipe.download("en-ewt") # download English model
        self.h_out = None
        self.is_tokenized = self.include_headers = False
        for sentence in doc.sentences:
            for idx, token in enumerate(sentence, 1):

text = "Barack Obama was born in Hawaii."
nlp = spacy_udpipe.load("en-ewt")

doc = nlp(text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
    def get_defaults(self, lang) -> Language.Defaults:




