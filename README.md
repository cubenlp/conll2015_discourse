A Refined Discourse Parser for CoNLL 2015 Shared Task
====================================================
A Refined End-to-End Discourse Parser participated in CoNLL 2015 Shared Task is described in the paper
[A Refined End-to-End Discourse Parser](http://aclweb.org/anthology/K15-2002) by Jianxiang Wang and Man Lan.

## Requirements

- [ETE](http://etetoolkit.org/)
- [MALLET](http://mallet.cs.umass.edu/)
- Python >= 2.7

## Usage


First, change the values of the following two variables in config.py: 


1. CWD: current working directory (absolute path).
1. MALLET_PATH: mallet bin path (absolute path).


Such as:
```
CWD = "/Users/XXX/Documents/conll2015_discourse/"
MALLET_PATH = "/Users/XXX/Documents/mallet"
```

Then, run the parser using the command in terminal as required by the [CoNLL 2015 Shared Task Official Blog](http://conll15st.blogspot.com/2015/03/discourse-parser-evaluation.html):
```
python $input_dataset $input_run $output_dir
```
- $input_dataset: the folder of the dataset to parse. The folder structure:

    $input_dataset/pdtb-parses.json
    
    $input_dataset/raw/...
- $input_run: the folder that contains the model file or other resources. Here, simply set it to 'none' in our parser.
- $output_dir: the folder that the parser will output 'output.json' to.

For example:
```
python parser.py data/conll15-st-03-04-15-dev none data
```
The parser will take the dataset under the  'data/conll15-st-03-04-15-dev' folder as input and 
generate a 'output.json' which contains the discourse relations parsed by the parser under the 'data' folder.


