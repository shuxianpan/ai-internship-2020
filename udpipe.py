import sys
import spacy_udpipe
from spacy.language import Language
from spacy.util import get_lang_class

class SpacyUdpipe:
    
    def __init__(self, lang):
        self.h_out = None
        self.nlp = spacy_udpipe.load(lang)
        self.tagmap = self.nlp.vocab.morphology.tag_map
        text = "Barack Obama was born in Hawaii. He was the president of the United States."
        self.doc = self.nlp(text)
        self.is_tokenized = self.include_headers = False
        
    def _get_morphology(self, tag):
        if not self.tagmap or tag not in self.tagmap:
            return '_'
        else:
            feats = [f'{prop}={val}' for prop, val in self.tagmap[tag].items() if not SpacyUdpipe._is_number(prop)]
            if feats:
                return '|'.join(feats)
            else:
                return '_'
                
    def _sentences_to_conllu(self, doc):
        for line_idx, sent in enumerate(doc.sents):
            line_idx += 1
            parsed_sent = ''

            if self.include_headers:
                parsed_sent = f'# sent_id = {str(line_idx)}\n'
                parsed_sent += f'# text = {sent.sent}\n'

            for idx, token in enumerate(sent, 1):
                if token.dep_.lower().strip() == 'root':
                    head_idx = 0
                else:
                    head_idx = token.head.i + 1 - sent[0].i

                line_tuple = (
                    idx,
                    token.text,
                    token.lemma_,
                    token.pos_,
                    token.tag_,
                    self._get_morphology(token.tag_),
                    head_idx,
                    token.dep_,
                    '_',
                    '_'
                )
                parsed_sent += '\t'.join(map(lambda x: str(x), line_tuple)) + '\n'

            if self.h_out is not sys.stdout:
                print(parsed_sent)

            yield line_idx, parsed_sent

    @staticmethod       
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

            



model = SpacyUdpipe("en-ewt")

lang = "en-ewt"

text = "Barack Obama was born in Hawaii. He was the president of the United States."

conll = model._sentences_to_conllu(model.doc)

list(conll)
