import stanza
from pathlib import Path
from stanza.utils.conll import CoNLL
from ufal.udpipe import Model, Pipeline # pylint: disable=no-name-in-module

class MainPipeline:

    def __init__(self, lang_or_model, nlp_str):

        if nlp_str == "stanza":
            self.nlp = stanza.Pipeline(lang_or_model, processors='tokenize,pos,lemma,depparse', use_gpu=True, pos_batch_size=2000, depparse_batch_size=2000)
        elif nlp_str == "udpipe":
            self.model = Model.load(lang_or_model)
            self.nlp = Pipeline(self.model, 'tokenize','tag','parse', 'conllu')

    def parse_to_conll(self, fin, nlp_str="stanza"):
        with open(fin, 'r', encoding="utf-8") as readinput:
            ri = readinput.read()

        if nlp_str == "stanza":
            doc = self.nlp(ri)
            dicts = doc.to_dict()
            conll = CoNLL.convert_dict(dicts)
        elif nlp_str == "udpipe":
            conll = self.nlp.process(ri)

        return conll

    def process_file(self, fin, nlp_str="stanza", out=None):

        out = Path('output.conllu') if out is None else Path(out)

        with out.open("w", encoding="utf-8") as myfile:

            output = self.parse_to_conll(fin,nlp_str)

            if nlp_str == "stanza":
                for sentence in output:
                    for word in sentence:
                        word_repr = '\t'.join(word)
                        myfile.write(f"{word_repr}\n")
                    myfile.write(f"\n")
            elif nlp_str == "udpipe":
                myfile.write(output)

        return out

def main(fin, lang_or_model, out, nlp_str="stanza"):

    parser = MainPipeline(lang_or_model, nlp_str)

    fout = parser.process_file(fin, nlp_str, out)

    print(f"Done processing file {fin} with {nlp_str}. Output written to {fout}")

if __name__ == '__main__':
    import argparse

    cparser = argparse.ArgumentParser(description="Pipeline to process data into CoNLL format for given NLP frameworks")
    cparser.add_argument("fin", help="Input file to parse")
    cparser.add_argument("-l", "--lang_or_model", help="Language of input file ", default="en")
    cparser.add_argument("-o", "--out",
                         help="Path to output file. If not given, will use input file with extension .conll")
    cparser.add_argument("-n", "--nlp_str", help="NLP framework to use", choices=["stanza", "udpipe"], default="stanza")

    cargs = vars(cparser.parse_args())
    main(**cargs)
