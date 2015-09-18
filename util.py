#coding:utf-8
import string
from multiprocessing import Process
from feature import Feature
from example import Example
from random import shuffle
import json
from tools.PorterStemmer import PorterStemmer
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

#Singleton，usage: @singleton...
def singleton(cls):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton



def getSpanIndecesInSent(span_tokens, sent_tokens):
    indice = []
    span_length = len(span_tokens); sent_length = len(sent_tokens)
    for i in xrange(len(sent_tokens)):
        if (i+span_length) <= sent_length  and sent_tokens[i:i+span_length] == span_tokens:
            indice.append(range(i,i+span_length))
    return indice

''' remove punctuation in string '''
def removePuctuation(s):
    exclude = string.punctuation + "``" + "''"
    s = ''.join(ch for ch in s if ch not in exclude)
    return s

''' run multiple threads'''
def run_multiple_threads(feature_function_list):
    procs = []
    for feat_fun in feature_function_list:
        p = Process(target = feat_fun)
        procs.append(p)
    for p in procs: p.start()
    for p in procs: p.join()

# merge all the features in the feature_list
def mergeFeatures(feature_list, name = ""):
    dimension = 0
    feat_string = ""
    for feature in feature_list:
        if dimension == 0:#第一个
            feat_string = feature.feat_string
        else:
            if feature.feat_string != "":
                #修改当前feature的index
                temp = ""
                for item in feature.feat_string.split(" "):
                    index, value = item.split(":")
                    temp += " %d:%s" % (int(index)+dimension, value)
                feat_string += temp
        dimension += feature.dimension

    merged_feature = Feature(name, dimension,{})
    merged_feature.feat_string = feat_string.strip()
    return merged_feature

# remove the item (value < threshold) from dict
def removeItemsInDict(dict, threshold = 1):
    if threshold > 1 :
        for key in dict.keys():
            if dict[key] < threshold:
                dict.pop(key)

# write dict keys to file
def write_dict_keys_to_file(dict, file_path):
    file_out = open(file_path,"w")
    file_out.write("\n".join([str(key) for key in dict.keys()]))
    file_out.close()

def load_list_from_file(list_file_path):
    list_file = open(list_file_path)
    list = [line.strip() for line in list_file]
    return list

def load_set_from_file(list_file_path):
    list_file = open(list_file_path)
    list = [line.strip() for line in list_file]
    return set(list)

# key : index
def load_dict_from_file(dict_file_path):
    dict = {}
    dict_file = open(dict_file_path)
    lines = [line.strip() for line in dict_file]
    for index, line in enumerate(lines):
        if line == "":
            continue
        dict[line] = index+1
    dict_file.close()
    return dict

def write_example_list_to_file(example_list, to_file):
    to_file = open(to_file, "w")
    to_file.write("\n".join([example.content + " # " + example.comment for example in example_list]))
    to_file.close()

def write_shuffled_example_list_to_file(example_list, to_file):
    shuffle(example_list)
    write_example_list_to_file(example_list, to_file)

def get_compressed_path(path):
    list = path.split("-->")
    temp = []
    for i in range(len(list)):
        if i+1 < len(list) and list[i] != list[i+1] :
            temp.append(list[i])
        if i+1 == len(list):
            temp.append(list[i])
    return "-->".join(temp)

def get_compressed_path_tag(path, Tag):
    list = path.split(Tag)
    temp = []
    for i in range(len(list)):
        if i+1 < len(list) and list[i] != list[i+1] :
            temp.append(list[i])
        if i+1 == len(list):
            temp.append(list[i])
    return Tag.join(temp)

def write_dict_list_to_json_file(dict_list, json_path):
    fout = open(json_path, 'w')
    strs = [json.dumps(innerdict) for innerdict in dict_list]
    s = "%s" % "\n".join(strs)
    fout.write(s)

#设置字典，value为key出现的频数
# set key value in dict where value is the frequency of the key
def set_dict_key_value(dict, key):
    if key not in dict:
        dict[key] = 0
    dict[key] += 1

def list_strip_punctuation(list):
    punctuation = """!"#&'*+,-..../:;<=>?@[\]^_`|~""" + "``" + "''"
    i = 0
    while i < len(list) and list[i][1] in punctuation + "-LCB--LRB-":
        i += 1
    if i == len(list):
        return []

    j = len(list) - 1
    while j >= 0 and list[j][1] in punctuation + "-RRB--RCB-":
        j -= 1

    return list[i: j+1]



def stem_string(line):
    if line == "":
        return ""
    p = PorterStemmer()
    word = ""
    output = ""
    for c in line:
        if c.isalpha():
            word += c.lower()
        else:
            if word:
                output += p.stem(word, 0,len(word)-1)
                word = ''
            output += c.lower()
    if word:
        output += p.stem(word, 0,len(word)-1)
    return output

def stem_list(list):
    return [stem_string(item) for item in list]


def cross_product(list1, list2):
    t = []
    for i in list1:
        for j in list2:
            t.append(i * j)
    return t

def is_number(number):
    return re.match(r"^(-?\d+)(\.\d+)?$", number) != None

def vec_plus_vec(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("vec1 and vec2 do not have the same length !")
    t = []
    for v1, v2 in zip(vec1, vec2):
        t.append(v1 + v2)
    return t

def lemma_word(word, pos):
    lmtzr = WordNetLemmatizer()

    word = word.lower()
    pos = get_wn_pos(pos)
    if pos == "":
        return word
    word = lmtzr.lemmatize(word, pos)

    return word

def get_wn_pos(tree_bank_tag):
    if tree_bank_tag.startswith('J'):
        return wordnet.ADJ
    elif tree_bank_tag.startswith('V'):
        return wordnet.VERB
    elif tree_bank_tag.startswith('N'):
        return wordnet.NOUN
    elif tree_bank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''