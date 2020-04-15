import sys
import spacy_udpipe
from spacy.language import Language
from spacy.util import get_lang_class

class SpacyUdpipe:
    
    def __init__(self, lang):
        self.h_out = None
        self.nlp = spacy_udpipe.load(lang)
        self.Defaults = get_defaults(lang)
        self.tagmap = self.Defaults.tag_map
        self.doc = self.nlp(text)
        self.is_tokenized = self.include_headers = False
        
    def _get_morphology(self, tag):
        if not self.tagmap or tag not in self.tagmap:
            return '_'
        else:
            feats = [f'{prop}={val}' for prop, val in self.tagmap[tag].items() if not Spacy2ConllParser._is_number(prop)]
            if feats:
                return '|'.join(feats)
            else:
                return '_'
                
    def _sentences_to_conllu(self, doc, line_idx):
        for sentence in doc.sentences:
            line_idx += 1
            parsed_sent = ''

            if self.include_headers:
                parsed_sent = f'# sent_id = {str(line_idx)}\n'
                parsed_sent += f'# text = {sentence.sentence}\n'

            for idx, token in enumerate(sentence, 1):
                if token.dep_.lower().strip() == 'root':
                    head_idx = 0
                else:
                    head_idx = token.head.i + 1 - sentence[0].i

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


    def get_defaults(self, lang) -> Language.Defaults:
    #Get the language-specific defaults, if available in spaCy. This allows
    #using lexical attribute getters that depend on static language data, e.g.
    #Token.like_num, Token.is_stop, Doc.noun_chunks, etc.
    #lang: ISO 639-1 language code or shorthand UDPipe model name.
    #RETURNS: The language defaults.
                try:
                    lang_cls = get_lang_class(lang)
                    return lang_cls.Defaults
                except ImportError:
                    return Language.Defaults

    @staticmethod       
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

            

spacy_udpipe.download("en-ewt") # download English model

model = SpacyUdpipe("en-ewt")

lang = "en-ewt"

text = "Barack Obama was born in Hawaii."

conll = model._sentences_to_conllu(doc)

print(conll)
