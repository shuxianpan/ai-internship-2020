import stanza
from stanza.utils.conll import CoNLL

stanza.download('en') # download English model
nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse') # initialize English neural pipeline
doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence

dicts = doc.to_dict()
conll = CoNLL.convert_dict(dicts)
print(conll)