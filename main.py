from pathlib import Path

import sys
import stanza
from stanza.utils.conll import CoNLL
import spacy_udpipe
from spacy.language import Language
from spacy.util import get_lang_class

class Pipeline:

    def __init__(self, lang, nlp_str):

        if nlp_str == "stanza":
            lang_or_model = "en"
            self.nlp = stanza.Pipeline(lang_or_model, processors='tokenize,pos,lemma,depparse', use_gpu=True, pos_batch_size=2000, depparse_batch_size=2000)

        elif nlp_str == "udpipe":
            #self.h_out = None
            lang_or_model = "en-ewt"
            self.nlp = spacy_udpipe.load(lang_or_model)
            self.tagmap = self.nlp.vocab.morphology.tag_map
            #self.is_tokenized = self.include_headers = False

    def _get_morphology(self, tag):

        if not self.tagmap or tag not in self.tagmap:
            return '_'

        else:
            feats = [prop.replace("_","=") for prop in self.tagmap[tag].keys() if not self._is_number(prop)]
            
            if feats:
                return '|'.join(feats)
            
            else:
                return '_'
                
    def _sentences_to_conllu(self, doc):

        for line_idx, sent in enumerate(doc.sents):
            line_idx += 1
            parsed_sent = ''

            #if self.include_headers:
                #parsed_sent = f'# sent_id = {str(line_idx)}\n'
                #parsed_sent += f'# text = {sent.sent}\n'

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

            yield f"#", parsed_sent

    def parse_to_conll(self, fin, nlp_str="stanza"):

        with open(fin, 'r', encoding="utf-8") as readinput:

            ri = readinput.read()

            doc = self.nlp(ri)

            if nlp_str == "stanza":
                dicts = doc.to_dict()
                conll = CoNLL.convert_dict(dicts)

            elif nlp_str == "udpipe":
                dicts = self._sentences_to_conllu(doc)
                conll = list(dicts)

            return conll

    def process_file(self, fin, nlp_str="stanza", out=None):
    # read file `fin`, process line for line with the correct `nlp`, write CoNLL output to `out`
    # return output file. It is either the given output file (if provided) or the same file path as the input file
    # but with extension .conll. Use pathlib for Path manipulation.

        out = Path('/output.conllu')

        with open('output.conllu', "w", encoding="utf-8") as myfile:

            output = self.parse_to_conll(fin,nlp_str)

            if nlp_str == "stanza":

                for sentence in output:
                    myfile.write(f"#\n")

                    for word in sentence:
                        word_repr = '\t'.join(word)
                        myfile.write(f"{word_repr}\n")
                        myfile.write(f"\n")

            elif nlp_str == "udpipe":

                for sents in output:

                    for token in sents:
                        myfile.write(f"{token}\n")
                
            return out

    @staticmethod       
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

def main(fin, lang, out, nlp_str="stanza"):

    parser = Pipeline(lang, nlp_str)

    fout = parser.process_file(fin, nlp_str, out)

    print(f"Done processing file {fin} with {nlp_str}. Output written to {fout}")

if __name__ == '__main__':
    import argparse

    cparser = argparse.ArgumentParser(description="Pipeline to process data into CoNLL format for given NLP frameworks")
    cparser.add_argument("fin", help="Input file to parse")
    cparser.add_argument("lang", help="Language of input file", default="en")
    cparser.add_argument("-o", "--out",
                         help="Path to output file. If not given, will use input file with extension .conll")
    # add others if necessary
    cparser.add_argument("-n", "--nlp_str", help="NLP framework to use", choices=["stanza", "udpipe"], default="stanza")

    cargs = vars(cparser.parse_args())
    main(**cargs)
