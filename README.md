A Refined Discourse Parser for CoNLL2015 Shared Task
====================================================
A Refined End-to-End Discourse Parser participated in CoNLL 2015 Shared Task is described in the paper
[A Refined End-to-End Discourse Parser](http://aclweb.org/anthology/K15-2002) by Jianxiang Wang and Man Lan.

## Requirements

- [ETE](http://etetoolkit.org/)
- [MALLET](http://mallet.cs.umass.edu/)
- Python >= 2.7

## Usage


First, change the values of the following two variables in config.py: 


1. CWD: current working directory:
1. MALLET_PATH: mallet bin path:


Such as:
```
CWD = "/Users/Hunter/Documents/pycharmSpace/CoNLL2015_final_submit/"
MALLET_PATH = "/Users/Hunter/Documents/conll2015/mallet"
```

Then, run the parser using the command as required by the CoNLL2015 organizers:
```
python input_dataset input_run output_dir
```
- input_dataset
- input_run
- output_dir

such as:
```
python parser.py data/conll15-st-03-04-15-dev none data
```
The parser will take the files under the  'data/conll15-st-03-04-15-dev' directory and 
generate a 'output.json' under the 'data' directory which contains the discourse relations parsed by the parser.


