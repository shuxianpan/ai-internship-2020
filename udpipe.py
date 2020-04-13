import sys
import spacy_udpipe

spacy_udpipe.download("en-ewt") # download English model
        self.h_out = None
        self.is_tokenized = self.include_headers = False

text = "Barack Obama was born in Hawaii."
nlp = spacy_udpipe.load("en-ewt")

doc = nlp(text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)




