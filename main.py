from pathlib import Path


def init_nlp(lang, nlp_str="stanza"):
    # initialize the correct parser with the correct language
    # return initialised parser

    import stanza
    from stanza.utils.conll import CoNLL
    stanza.download('en') # download English model
    nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse') # initialize English neural pipeline
    doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence
    dicts = doc.to_dict()
    conll = CoNLL.convert_dict(dicts)


    return nlp


def process_file(fin, nlp, out=None):
    # read file `fin`, process line for line with the correct `nlp`, write CoNLL output to `out`
    # return output file. It is either the given output file (if provided) or the same file path as the input file
    # but with extension .conll. Use pathlib for Path manipulation.
    return out


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
