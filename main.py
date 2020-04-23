from pathlib import Path

import sys
import stanza
from stanza.utils.conll import CoNLL
import spacy_udpipe
from spacy.language import Language
from spacy.util import get_lang_class


def init_nlp(lang, nlp_str="stanza"):
    # initialize the correct parser with the correct language
    # return initialised parser
    if nlp_str="stanza":
        lang = 'en'
        stanza = stanza.download(lang)
        nlp = stanza
        elif nlp_str="udpipe":
            lang = "en-ewt"
            udpipe = spacy_udpipe.download(lang)
            nlp = udpipe

    return nlp


def process_file(fin, nlp, out=None):
    # read file `fin`, process line for line with the correct `nlp`, write CoNLL output to `out`
    # return output file. It is either the given output file (if provided) or the same file path as the input file
    # but with extension .conll. Use pathlib for Path manipulation.
    p = Path('/en_ewt-ud-test.txt')
    with p.open('r', encoding="utf-8") as f:
            fin = f.read()
            f.closed

            output = Pipeline.parse_to_conll(doc)

            with open('output.conllu', "w", encoding="utf-8") as myfile:
                if nlp = stanza:
                    for sentence in output:
                        myfile.write(f"#\n")
                        for word in sentence:
                            word_repr = '\t'.join(word)
                            myfile.write(f"{word_repr}\n")
                            myfile.write(f"\n")
                    elif nlp = udpipe:
                        for sents in output:
                            for token in sents:
                                myfile.write(f"{token}\n")
                out = Path('/output.conllu')

                return out

class Pipeline:
    def __init__(self, <arguments that are in the argparse>):
        self.nlp_type = nlp
        if nlp == ‘stanza’:
            self.nlp = stanza.Pipeline(lang, processors='tokenize,pos,lemma,depparse') # initialize English neural pipeline
            elif nlp == ‘udpipe’:
                self.h_out = None
                self.nlp = spacy_udpipe.load(lang)
                self.tagmap = self.nlp.vocab.morphology.tag_map
                self.is_tokenized = self.include_headers = False
    
    def _get_morphology(self, tag):
        if not self.tagmap or tag not in self.tagmap:
            return '_'
        else:
            feats = [prop.replace("_","=") for prop in self.tagmap[tag].keys() if not SpacyUdpipe._is_number(prop)]
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

            yield f"# sent_id = {line_idx}", parsed_sent

    def parse_to_conll(self, doc):
        doc = self.nlp(fin)
        if nlp == ‘stanza’:
            dicts = doc.to_dict()
            conll = CoNLL.convert_dict(dicts)
            return conll
            elif nlp == ‘udpipe’:
                conll = self._sentences_to_conllu(doc)
                list(conll)

    @staticmethod       
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

def main(fin, lang, out=None, nlp_str="stanza"):
    nlp = init_nlp(lang, nlp_str)

    fout = process_file(fin, nlp, out)

    print(f"Done processing file {fin} with {nlp_str}. Output written to {fout}")

if __name__ == '__main__':
    import argparse

    cparser = argparse.ArgumentParser(description="Pipeline to process data into CoNLL format for given NLP frameworks")
    cparser.add_argument("fin", help="Input file to parse")
    cparser.add_argument("lang", help="Language of input file")
    cparser.add_argument("-o", "--out",
                         help="Path to output file. If not given, will use input file with extension .conll")
    # add others if necessary
    cparser.add_argument("-n", "--nlp_str", help="NLP framework to use", choices=["stanza", "udpipe"], default="stanza")

    cargs = vars(cparser.parse_args())
    main(**cargs)
