import spacy_udpipe

spacy_udpipe.download("en-ewt") # download English model

text = "Barack Obama was born in Hawaii."
nlp = spacy_udpipe.load("en-ewt")

doc = nlp(text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)

class SpacyUdpipe:
def __init__(self, path):

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
        for sent in doc.sents:
            line_idx += 1
            parsed_sent = ''

            if self.include_headers:
                parsed_sent = f'# sent_id = {str(line_idx)}\n'
                parsed_sent += f'# text = {sent.sent}\n'

            for idx, word in enumerate(sent, 1):
                if word.dep_.lower().strip() == 'root':
                    head_idx = 0
                else:
                    head_idx = word.head.i + 1 - sent[0].i

                line_tuple = (
                    idx,
                    word.text,
                    word.lemma_,
                    word.pos_,
                    word.tag_,
                    self._get_morphology(word.tag_),
                    head_idx,
                    word.dep_,
                    '_',
                    '_'
                )
                parsed_sent += '\t'.join(map(lambda x: str(x), line_tuple)) + '\n'

            if self.h_out is not sys.stdout and self.verbose:
                print(parsed_sent)

            yield line_idx, parsed_sent

@staticmethod
def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False


