# ai-internship-2020
This is a pipeline for accessing to `UDPipe` and `Stanza` pipeline via one Python script, and have a CoNLL-U file as the parsing output. The default tool is `Stanza`. The default model is the default English model for `Stanza`. 

To use the pipeline, please download the models to local first, and run `main.py` in command prompt. Use the arguments to change the setting of tools, models, and output path:

```
main.py --h
usage: main.py [-h] [-l LANG_OR_MODEL] [-o OUT] [-n {stanza,udpipe}] fin

Pipeline to process data into CoNLL format for given NLP frameworks

positional arguments:
  fin                   Input file to parse

optional arguments:
  -h, --help            show this help message and exit
  -l LANG_OR_MODEL, --lang_or_model LANG_OR_MODEL
                        Language of input file
  -o OUT, --out OUT     Path to output file. If not given, will use input file
                        with extension .conll
  -n {stanza,udpipe}, --nlp_str {stanza,udpipe}
                        NLP framework to use
```                        
 
`pipeline-old.py` is the earlier version of the pipeline, using `spaCY-UDPipe`. Note that the UPOS tags and UFeats in its output file are based on automatic `tag_map`, so the accuracy is less reliable.
