import stanza

from stanza.utils.conll import CoNLL

def _stanza_pipeline(lang,text):
    nlp = stanza.Pipeline(lang, processors='tokenize,pos,lemma,depparse') # initialize English neural pipeline
    doc = nlp(text) # run annotation over a sentence
    dicts = doc.to_dict()
    conll = CoNLL.convert_dict(dicts)
    return conll

#lang = 'en'
#text = 'Barack Obama was born in Hawaii. He was the president of the United States.'
#c = _stanza_pipeline(lang,text)
#print(c)