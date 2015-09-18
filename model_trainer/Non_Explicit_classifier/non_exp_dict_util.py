#coding:utf-8
import util
from syntax_tree import Syntax_tree
from non_explicit_dict import Non_Explicit_dict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from connective_dict import Connectives_dict
from operator import itemgetter

def get_word_pairs(relation, parse_dict):
    Arg1_words = get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = get_Arg_Words_List(relation, "Arg2", parse_dict)

    #stem
    Arg1_words = util.stem_list(Arg1_words)
    Arg2_words = util.stem_list(Arg2_words)

    word_pairs = []
    for word1 in Arg1_words:
        for word2 in Arg2_words:
            word_pairs.append("%s|%s" % (word1, word2))
    return word_pairs

def get_brown_cluster_pairs(relation, parse_dict):
    Arg1_words = get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = get_Arg_Words_List(relation, "Arg2", parse_dict)

    dict_brown_cluster = Non_Explicit_dict().brown_cluster

    brown_cluster_pairs = []
    for word1 in Arg1_words:
        for word2 in Arg2_words:
            if word1 in dict_brown_cluster and word2 in dict_brown_cluster:
                brown_cluster_pairs.append("%s|%s" % (dict_brown_cluster[word1], dict_brown_cluster[word2]))

    return brown_cluster_pairs


# def get_production_rules(relation, parse_dict):
#     Arg1_production_rules = get_Arg_production_rules(relation, "Arg1", parse_dict)
#     Arg2_production_rules = get_Arg_production_rules(relation, "Arg2", parse_dict)
#
#     return Arg1_production_rules + Arg2_production_rules

def get_production_rules(relation, parse_dict):
    Arg1_production_rules = get_Arg_production_rules(relation, "Arg1", parse_dict)
    Arg2_production_rules = get_Arg_production_rules(relation, "Arg2", parse_dict)
    rules = Arg1_production_rules + Arg2_production_rules

    production_rules = ["Arg1_%s" % rule for rule in rules] + \
                       ["Arg2_%s" % rule for rule in rules] + \
                       ["Both_%s" % rule for rule in rules]

    return production_rules

def get_arg_brown_cluster(relation, parse_dict):
    Arg1_brown_cluster = get_Arg_brown_cluster(relation, "Arg1", parse_dict)
    Arg2_brown_cluster = get_Arg_brown_cluster(relation, "Arg2", parse_dict)

    cluster = Arg1_brown_cluster + Arg2_brown_cluster

    brown_cluster = ["Arg1_%s" % x for x in cluster] + \
                   ["Arg2_%s" % x for x in cluster] + \
                   ["Both_%s" % x for x in cluster]

    return brown_cluster

def get_Arg_brown_cluster(relation, Arg, parse_dict):
    Arg_words = get_Arg_Words_List(relation, Arg, parse_dict)
    dict_brown_cluster = Non_Explicit_dict().brown_cluster
    Arg_brown_cluster = []
    for word in Arg_words:
        if word in dict_brown_cluster:
            Arg_brown_cluster.append(dict_brown_cluster[word])
    return Arg_brown_cluster


def get_cp_production_rules(relation, parse_dict):
    Arg1_production_rules = get_Arg_production_rules(relation, "Arg1", parse_dict)
    Arg2_production_rules = get_Arg_production_rules(relation, "Arg2", parse_dict)

    cp = []
    for rule1 in Arg1_production_rules:
        for rule2 in Arg2_production_rules:
            cp.append("%s|%s" % (rule1, rule2))

    return cp

def get_Arg_production_rules(relation, Arg, parse_dict):
    #1.  dict[(DocID, sent_index)] = [token_list]
    dict = {}
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        if (DocID, sent_index) not in dict:
            dict[(DocID, sent_index)] = [word_index]
        else:
            dict[(DocID, sent_index)].append(word_index)

    #2.
    Arg_subtrees = []
    for (DocID, sent_index) in dict.keys():
        parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
        syntax_tree = Syntax_tree(parse_tree)
        if syntax_tree.tree != None:
            Arg_indices = dict[(DocID, sent_index) ]
            Arg_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in Arg_indices])

            no_need = []
            for node in syntax_tree.tree.traverse(strategy="levelorder"):
                if node not in no_need:
                    if set(node.get_leaves()) <= Arg_leaves:
                        Arg_subtrees.append(node)
                        no_need.extend(node.get_descendants())


    production_rule = []
    for tree in Arg_subtrees:
        for node in tree.traverse(strategy="levelorder"):
            if not node.is_leaf():
                rule = node.name + "-->" + " ".join([child.name for child in node.get_children()])
                production_rule.append(rule)

    return production_rule


def get_dependency_rules(relation, parse_dict):
    Arg1_dependency_rules = get_Arg_dependency_rules(relation, "Arg1", parse_dict)
    Arg2_dependency_rules = get_Arg_dependency_rules(relation, "Arg2", parse_dict)
    return Arg1_dependency_rules + Arg2_dependency_rules

def get_Arg_dependency_rules(relation, Arg, parse_dict):
    #1.  dict[(DocID, sent_index)] = [token_list]
    dict = {}
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        if (DocID, sent_index) not in dict:
            dict[(DocID, sent_index)] = [word_index]
        else:
            dict[(DocID, sent_index)].append(word_index)

    dependency_rules = []
    for (DocID, sent_index) in dict:
        Arg_indices = [item+1 for item in dict[(DocID, sent_index)]]#dependency 从1开始
        dependency_list = parse_dict[DocID]["sentences"][sent_index]["dependencies"]

        depen_dict = {}# depen_dict["talk"] = ["nsubj", "aux"]
        for dependency in dependency_list:
            if int(dependency[1].split("-")[-1]) in Arg_indices:
                word = "-".join(dependency[1].split("-")[:-1])
                if word not in depen_dict:
                    depen_dict[word] = [dependency[0]]
                else:
                    depen_dict[word].append(dependency[0])
        for key in depen_dict:
            rule = key + "<--" + " ".join(depen_dict[key])
            dependency_rules.append(rule)
        # print dependency_rules
    return dependency_rules


#[(sent_index, index)]
# Arg : Arg1 or Arg2
def get_Arg_TokenList(relation, Arg):
    return [(item[3], item[4]) for item in relation[Arg]["TokenList"]]

#['I', 'love', 'China']
def get_Arg_Words_List(relation, Arg, parse_dict):
    words = []
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][0]
        words.append(word)
    return words

#['NN', 'VERB', '''']
def get_Arg_POS_List(relation, Arg, parse_dict):
    pos = []
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        pos_tag = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"]
        pos.append(pos_tag)
    return pos

#['PERSON', 'LOCATION', '''']
def get_Arg_NER_TAG_List(relation, Arg, parse_dict):
    ner_tag = []
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        tag = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][1]["NER_TAG"]
        ner_tag.append(tag)
    return ner_tag

def get_firstlast_first3(relation, parse_dict):
    Arg1_words = get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = get_Arg_Words_List(relation, "Arg2", parse_dict)
    Arg1_first = Arg1_words[0]
    Arg1_last = Arg1_words[-1]
    Arg2_first = Arg2_words[0]
    Arg2_last = Arg2_words[-1]
    if len(Arg1_words) >= 3:
        Arg1_first3 = "_".join(Arg1_words[:3])
    else:
        Arg1_first3 = "_".join(Arg1_words + ["NULL"]*(3-len(Arg1_words)))
    if len(Arg2_words) >= 3:
        Arg2_first3 = "_".join(Arg2_words[:3])
    else:
        Arg2_first3 = "_".join(Arg2_words + ["NULL"]*(3-len(Arg2_words)))

    Arg1_first_Arg2_first = "%s|%s" % (Arg1_first, Arg2_first)
    Arg1_last_Arg2_last = "%s|%s" % (Arg1_last, Arg2_last)

    return Arg1_first, Arg1_last, Arg2_first, Arg2_last, Arg1_first_Arg2_first, Arg1_last_Arg2_last, Arg1_first3, Arg2_first3


def get_modality_vec(words_list):
    dict_modality = {"can": 1, "may": 2, "must": 3, "need": 4, "shall": 5, "will": 6,
                    "could": 1, "would": 6, "might": 2, 'should': 5, "'ll": 5, "wo": 6, "sha": 5, "ca": 1,
                    "have to": 7, "had to": 7, "'d to": 7, "'ve to": 7
    }
    list = [0]*7
    length = len(words_list)
    for index, word in enumerate(words_list):
        word = word.lower()
        if word in dict_modality:
            list[dict_modality[word]-1] = 1
        if index != length -1:
            t = "%s %s" % (word, words_list[index + 1])
            if t in dict_modality:
                list[dict_modality[t]-1] = 1

    return list




def get_main_verb_pos(relation, Arg, parse_dict):

    MV_dict = {"MD":1, "VB":2, "VBD":3, "VBG":4, "VBN":5, "VBP":6, "VBZ":7}

    list = [0] * 7
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        #获取对应的pos tag
        pos_tag = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"]
        if pos_tag in MV_dict:
            list[MV_dict[pos_tag] - 1] = 1
            break
    return list

def get_main_verb_pair(relation, parse_dict):
    arg1_main_verb = _get_main_verb(relation, "Arg1", parse_dict)
    arg2_main_verb = _get_main_verb(relation, "Arg2", parse_dict)
    return "%s|%s" % (arg1_main_verb, arg2_main_verb)


#
def _get_main_verb(relation, Arg, parse_dict):

    verb_pos = ["VBD", "VBN"] + ["VB", "VBP", "VBZ"] + ["VBG"]

    be_have_words = ["have", "has", "had", "'ve", "'d", "is", "am", "are", "was", "were", "been", "be", "'s", "'re", "'m"]

    word_list = get_Arg_Words_List(relation, Arg, parse_dict)
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    # verb, but not: be have
    for word, pos in zip(word_list, pos_list):
        if pos in verb_pos and word not in be_have_words:
            word = util.lemma_word(word, pos)
            return word
    # only: be have
    for word, pos in zip(word_list, pos_list):
        if word in be_have_words:
            word = util.lemma_word(word, pos)
            return word

    return "None"

def get_inquirer_vec(relation, Arg, parse_dict):
    inquirer = Non_Explicit_dict().inquirer
    inquirer_stem = Non_Explicit_dict().inquirer_stem

    list = [0] * 42
    verb_tag= ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    # ["NN/dog" ,"NNS/joks]
    word_list = _get_Arg_word_pos_list(relation, Arg, parse_dict)

    for item in word_list:
        if item == "":
            continue
        tag, word = item.split("/")[:2]
        if tag not in verb_tag:
            continue
        word = word.lower()
        if word in inquirer.keys():
            list = _merge(list, inquirer[word])
        else:
            stem = util.stem_string(word)
            if stem in inquirer.keys():
                list = _merge(list, inquirer[stem])
            elif stem in inquirer_stem.keys():
                list = _merge(list, inquirer_stem[stem])

    return list

def _merge(list_a, list_b):
        list = []
        for i in range(len(list_a)):
            if list_b[i] == "1":
                list.append(1)
            else:
                list.append(list_a[i])
        return list



def _get_Arg_word_pos_list(relation, Arg, parse_dict):
    word_list = []
    DocID = relation["DocID"]
    Arg_TokenList = get_Arg_TokenList(relation, Arg)
    for sent_index, word_index in Arg_TokenList:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][word_index][1]["PartOfSpeech"]
        word_list.append("%s/%s" % (pos, word))
    return word_list


def get_polarity_vec(relation, Arg, parse_dict):
    dict = {"negatepositive": 0, "positive": 1, "negative": 2, "neutral": 3}
    list = [0] * 4
    index = 0
    word_list = get_Arg_Words_List(relation, Arg, parse_dict)

    for i in range(len(word_list)):
        word = word_list[i]
        polarity_list = get_polarity(word)
        if len(polarity_list) == 0:
            continue
        for polarity in polarity_list:
            if polarity == "positive":
                if is_negate(word_list[index:i]):
                    polarity = "negatepositive"
            index = i
            list[dict[polarity]] = 1
    return list

def get_polarity(word):
    polarity = Non_Explicit_dict().polarity
    polarity_stem = Non_Explicit_dict().polarity_stem

    pol = ""
    if word in polarity:
        pol = polarity[word]
    else:
        stem = util.stem_string(word)
        if stem in polarity:
            pol = polarity[stem]
        if stem in polarity_stem:
            pol = polarity_stem[stem]
    if pol == "":
        return []
    else:
        return pol.split("|")

def is_negate(wordlist):
    negate = Non_Explicit_dict().negate
    negate_stem = Non_Explicit_dict().negate_stem

    for word in wordlist:
        if word in negate:
            return True
        else:
            stem = util.stem_string(word)
            if stem in negate or stem in negate_stem:
                return True
    return False

# in:('humor', 'verb') ; out: ('strongsubj', 'positive')
def get_word_MPQA_polarity(word_pos_tuple):
    n_stemmed_word_pos_dict = Non_Explicit_dict().n_stemmed_word_pos_dict
    y_stemmed_word_pos_dict = Non_Explicit_dict().y_stemmed_word_pos_dict

    word, pos = word_pos_tuple

    if word_pos_tuple in n_stemmed_word_pos_dict:
        return n_stemmed_word_pos_dict[word_pos_tuple]
    elif (word, "anypos") in n_stemmed_word_pos_dict:
        return n_stemmed_word_pos_dict[(word, "anypos")]

    # stem
    word = util.stem_string(word)
    if (word, pos) in y_stemmed_word_pos_dict:
        return y_stemmed_word_pos_dict[(word, pos)]
    elif (word, "anypos") in y_stemmed_word_pos_dict:
        return y_stemmed_word_pos_dict[(word, "anypos")]

    # no match
    return ("NULL", "NULL")

def get_MPQA_polarity_vec(relation, Arg, parse_dict):
    polarity_cate = ["negatepositive", "positive", "negative", "neutral"]
    subj_cate = ["strongsubj", "weaksubj"]

    dict = {}
    t = 0
    for p in polarity_cate:
        for s in subj_cate:
            dict["%s_%s" % (s, p)] = t
            t += 1

    list = [0] * len(dict)

    word_list = [word.lower() for word in get_Arg_Words_List(relation, Arg, parse_dict)]
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    for index, (word, pos) in enumerate(zip(word_list, pos_list)):
        subj, polarity = get_word_MPQA_polarity((word, pos))# ('strongsubj', 'positive')
        if polarity in ["NULL", "both"]:
            continue
        # negate positive
        if polarity == "positive" and is_negate_MPQA(index, word_list):
            polarity = "negatepositive"

        subj_polarity = "%s_%s" % (subj, polarity)
        # count or not
        list[dict[subj_polarity]] = 1


    return list

def get_MPQA_polarity_score_vec(relation, Arg, parse_dict):
    polarity_cate = ["negatepositive", "positive", "negative", "neutral", "both"]

    polarity_dict = dict(zip(polarity_cate, range(5)))

    list = [0] * len(polarity_dict)

    word_list = [word.lower() for word in get_Arg_Words_List(relation, Arg, parse_dict)]
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    for index, (word, pos) in enumerate(zip(word_list, pos_list)):
        subj, polarity = get_word_MPQA_polarity((word, pos))# ('strongsubj', 'positive')
        if polarity == "NULL":
            continue
        # negate positive
        if polarity == "positive" and is_negate_MPQA(index, word_list):
            polarity = "negatepositive"


        # strong ＋2， weak ＋1
        if subj == "strongsubj":
            list[polarity_dict[polarity]] += 2
        if subj == "weaksubj":
            list[polarity_dict[polarity]] += 1

    return list

def get_MPQA_polarity_no_strong_weak_vec(relation, Arg, parse_dict):
    polarity_cate = ["negatepositive", "positive", "negative", "neutral", "both"]

    polarity_dict = dict(zip(polarity_cate, range(5)))

    list = [0] * len(polarity_dict)

    word_list = [word.lower() for word in get_Arg_Words_List(relation, Arg, parse_dict)]
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    for index, (word, pos) in enumerate(zip(word_list, pos_list)):
        subj, polarity = get_word_MPQA_polarity((word, pos))# ('strongsubj', 'positive')
        if polarity == "NULL":
            continue
        # negate positive
        if polarity == "positive" and is_negate_MPQA(index, word_list):
            polarity = "negatepositive"

        list[polarity_dict[polarity]] += 1

    return list


def is_negate_MPQA(index, word_list):
    negate_words = Non_Explicit_dict().negate
    prev1 = "NULL"; prev2 = "NULL"; prev3 = "NULL"
    if index - 1 >= 0:
        prev1 = word_list[index - 1]
    if index - 2 >= 0:
        prev2 = word_list[index - 2]
    if index - 3 >= 0:
        prev3 = word_list[index - 3]

    prev_words = [prev1, prev2, prev3]

    if set(prev_words) & set(negate_words) != set([]):
        return True
    else:
        return False





def get_all_words(relation, parse_dict):

    return get_Arg_Words_List(relation, "Arg1", parse_dict) +\
           get_Arg_Words_List(relation, "Arg2", parse_dict)

def get_lower_case_lemma_words(relation, parse_dict):

    return _get_lower_case_lemma_words(relation, "Arg1", parse_dict) +\
           _get_lower_case_lemma_words(relation, "Arg2", parse_dict)

def _get_lower_case_lemma_words(relation, Arg, parse_dict):
    Arg_words = get_Arg_Words_List(relation, Arg, parse_dict)
    Arg_pos = get_Arg_POS_List(relation, Arg, parse_dict)

    lmtzr = WordNetLemmatizer()

    lower_case_lemma_words = []
    for pos, word in zip(Arg_pos, Arg_words):
        word = word.lower()
        pos = get_wn_pos(pos)
        if pos == "":
            continue
        word = lmtzr.lemmatize(word, pos)
        lower_case_lemma_words.append(word)

    return lower_case_lemma_words

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

def get_word2vec_cluster_pairs(relation, parse_dict):
    Arg1_words = get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = get_Arg_Words_List(relation, "Arg2", parse_dict)

    dict_word2vec_cluster = Non_Explicit_dict().word2vec_cluster

    word2vec_cluster_pairs = []
    for word1 in Arg1_words:
        for word2 in Arg2_words:
            if word1 in dict_word2vec_cluster and word2 in dict_word2vec_cluster:
                word2vec_cluster_pairs.append("%s|%s" % (dict_word2vec_cluster[word1], dict_word2vec_cluster[word2]))

    return word2vec_cluster_pairs


def get_arg_first3_conn_pair(relation, parse_dict):
    arg1_first3_conn = _get_Arg_first3_conn(relation, "Arg1", parse_dict)
    arg2_first3_conn = _get_Arg_first3_conn(relation, "Arg2", parse_dict)

    return "%s_%s" % (arg1_first3_conn, arg2_first3_conn)

def get_arg1_first3_conn(relation, parse_dict):
    return _get_Arg_first3_conn(relation, "Arg1", parse_dict)

def get_arg2_first3_conn(relation, parse_dict):
    return _get_Arg_first3_conn(relation, "Arg2", parse_dict)



# def _get_Arg_first3_conn(relation, Arg, parse_dict):
#     word_list = get_Arg_Words_List(relation, Arg, parse_dict)
#     first3_words = word_list[:3]#少于3个的,没关系，python会处理。即会返回如［1，2］
#     conn_names, _ = _check_connective_names(first3_words)
#
#     if conn_names != []:
#         return conn_names[0]
#     else:
#         return "NULL"

def _get_Arg_first3_conn(relation, Arg, parse_dict):
    word_list = get_Arg_Words_List(relation, Arg, parse_dict)
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    first3_words = word_list[:3]
    conn_names, indices = _check_connective_names(first3_words)

    if conn_names != []:
        pos = " ".join([pos_list[index] for index in indices[0]])
        conn = conn_names[0]
        return "%s_%s" % (conn, pos)
    else:
        return "NULL_NULL"

def get_arg1_tense(relation, parse_dict):
    return _get_Arg_tense(relation, "Arg1", parse_dict)

def get_arg2_tense(relation, parse_dict):
    return _get_Arg_tense(relation, "Arg2", parse_dict)


def get_arg1_arg2_tense_pair(relation, parse_dict):
    Arg1_tense = _get_Arg_tense(relation, "Arg1", parse_dict)
    Arg2_tense = _get_Arg_tense(relation, "Arg2", parse_dict)

    return "%s|%s" % (Arg1_tense, Arg2_tense)

def _get_Arg_tense(relation, Arg, parse_dict):
    word_list = [word.lower() for word in get_Arg_Words_List(relation, Arg, parse_dict)]
    pos_list = get_Arg_POS_List(relation, Arg, parse_dict)

    return _get_coarse_tense(get_tense_in_sent(zip(word_list, pos_list)))


#[("I", "PRP"), ("love", "VBP"), ("China", "NNP")]
def get_tense_in_sent(word_pos_list):

    tense = "NULL"

    past_verb_pos = ["VBD", "VBN"] #过去时
    present_verb_pos = ["VB", "VBP", "VBZ"]#现在时
    continuous_verb_pos = ["VBG"]# 进行时
    verb_pos = past_verb_pos + present_verb_pos + continuous_verb_pos

    be_have_words = ["have", "has", "had", "'ve", "'d", "is", "am", "are", "was", "were", "been", "be", "'s", "'re", "'m"]

    flag = 0
    #1. 先去找不是 have, has, had, 've, 'd, is, am, are, was, were, been, be, 's, 're 'm 的动词
    for index, (word, pos) in enumerate(word_pos_list):
        if pos in verb_pos and word not in be_have_words:
            if pos in past_verb_pos:#过去式，1.现在完成时 2.过去完成式 3.将来完成时 4.一般过去时
                #查看前面三个词
                prev_1 = "NULL"
                prev_2 = "NULL"
                prev_3 = "NULL"
                if index - 1 >= 0:
                    prev_1 = word_pos_list[index - 1][0]
                if index - 2 >= 0:
                    prev_2 = word_pos_list[index - 2][0]
                if index - 3 >= 0:
                    prev_3 = word_pos_list[index - 3][0]

                if prev_1 in ["have", "has", "'ve"] or prev_2 in ["have", "has", "'ve"]:
                    tense = "perfect_present"

                if prev_1 in ["had", "'d"] or prev_2 in ["had", "'d"]:
                    tense = "perfect_past"

                #将来完成时 will have done/ won't have done
                if prev_1 == "have":
                    if prev_2 in ["will", "'ll", "wo"] or prev_3 in ["will", "'ll", "wo"]:
                        tense = "perfect_future"

                if "perfect" not in tense: # 一般过去时
                    tense = "simple_past"

            if pos in present_verb_pos: # 现在时
                #查看前面二个词
                prev_1 = "NULL"
                prev_2 = "NULL"
                if index - 1 >= 0:
                    prev_1 = word_pos_list[index - 1][0]
                if index - 2 >= 0:
                    prev_2 = word_pos_list[index - 2][0]
                if prev_1 in ["will", "'ll", "wo"] or prev_2 in ["will", "'ll", "wo"]:
                    tense = "simple_future"
                else:
                    tense = "simple_present"

            if pos in continuous_verb_pos: # 进行时
                #查看前面三个词
                prev_1 = "NULL"
                prev_2 = "NULL"
                prev_3 = "NULL"
                prev_4 = "NULL"
                if index - 1 >= 0:
                    prev_1 = word_pos_list[index - 1][0]
                if index - 2 >= 0:
                    prev_2 = word_pos_list[index - 2][0]
                if index - 3 >= 0:
                    prev_3 = word_pos_list[index - 3][0]
                if index - 4 >= 0:
                    prev_4 = word_pos_list[index - 4][0]

                # 过去进行
                if prev_1 in ["was", "were"] or prev_2 in ["was", "were"]:
                    tense = "continuous_past"
                # 现在进行
                if prev_1 in ["am", "is", "are", "'s", "'m", "'re"] or prev_2 in ["am", "is", "are", "'s", "'m", "'re"]:
                    tense = "continuous_present"
                # 将来进行时
                if prev_1 == "be":
                    if prev_2 in ["will", "'ll", "wo"] or prev_3 in ["will", "'ll", "wo"]:
                        tense = "continuous_future"
                # 过去完成进行时
                if prev_1 == "been":
                    if prev_2 in ["had", "'d"] or prev_3 in ["had", "'d"]:
                        tense = "perfect_continuous_past"
                # 现在完成进行时
                if prev_1 == "been":
                    if prev_2 in ["have", "has", "'ve", "'s"] or prev_3 in ["have", "has", "'ve", "'s"]:
                        tense = "perfect_continuous_present"
                # 将来完成进行时 will have been
                if prev_2 == "have" and prev_1 == "been":
                    if prev_3 in ["will", "'ll", "wo"] or prev_4 in ["will", "'ll", "wo"]:
                        tense = "perfect_continuous_future"

            flag = 1 #找到了
            break#找第一个动词

    if flag == 0: #没有找到除be，have之外的动词
        #找 be ,have
        for index, (word, pos) in enumerate(word_pos_list):
            if word in be_have_words:# ["have", "has", "had", "'ve", "'d", "is", "am", "are", "was", "were", "been", "be", "'s", "'re", "'m"]
                #直接根据pos判断
                if pos in past_verb_pos:
                    tense = "simple_past"
                if pos in present_verb_pos:
                    tense = "simple_present"

    return tense

# tense只分 past , present, future
def _get_coarse_tense(tense):
    if "past" in tense:
        return "past"

    if "present" in tense:
        return "present"

    if "future" in tense:
        return "future"

    return "NULL"

# identify connectives in the sentence, and return their names: ["but", "in particular"]
def _check_connective_names(sent_tokens):
    sent_tokens = [word.lower() for word in sent_tokens ]
    indices = []
    conn_names = []
    tagged = set([])
    sortedConn = Connectives_dict().sorted_conns_list
    for conn in sortedConn:
        if '..' in conn:
            c1, c2 = conn.split('..')
            c1_indice = util.getSpanIndecesInSent(c1.split(), sent_tokens)#[[7]]
            c2_indice = util.getSpanIndecesInSent(c2.split(), sent_tokens)#[[10]]
            if c1_indice!= [] and c2_indice != []:
                if c1_indice[0][0] < c2_indice[0][0]:
                    temp = set([t for t in (c1_indice[0]+c2_indice[0]) ])
                    if tagged & temp == set([]):
                        indices.append(c1_indice[0]+c2_indice[0])# [[7], [10]]
                        conn_names.append(conn)
                        tagged = tagged.union(temp)
        else:
            c_indice = util.getSpanIndecesInSent(conn.split(), sent_tokens)#[[2,6],[1,3],...]
            if c_indice !=[]:
                tt = []
                for item in c_indice:
                    if set(item) & tagged == set([]):
                        tt.append(item)
                c_indice = tt

                if c_indice != []:
                    indices.extend([item for item in c_indice])#[([2,6], 'for instance'), ....]
                    tagged = tagged.union(set([r for t in c_indice for r in t]))
                    conn_names.append(conn)
    return conn_names , indices




# dict[(DocID, sent1_index, sent2_index)] = [(conn_indices_string, conn, sense)]
def get_prev_context_conn(relation, parse_dict, non_explicit_context_dict):
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    if Arg1_sent_index - 1 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 1, Arg1_sent_index - 1) in non_explicit_context_dict:
        _list = non_explicit_context_dict[(DocID, Arg1_sent_index - 1, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][1]

    if Arg1_sent_index - 2 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 2, Arg1_sent_index - 1) in non_explicit_context_dict:
        _list = non_explicit_context_dict[(DocID, Arg1_sent_index - 2, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][1]

    return "NULL"

# dict[(DocID, sent1_index, sent2_index)] = [(conn_indices_string, conn, sense)]
def get_prev_context_sense(relation, parse_dict, implicit_context_dict):
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    if Arg1_sent_index - 1 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 1, Arg1_sent_index - 1) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg1_sent_index - 1, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][2]

    if Arg1_sent_index - 2 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 2, Arg1_sent_index - 1) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg1_sent_index - 2, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][2]

    return "NULL"

# conn + sense
# dict[(DocID, sent1_index, sent2_index)] = [(conn_indices_string, conn, sense)]
def get_prev_context_conn_sense(relation, parse_dict, implicit_context_dict):
    DocID = relation["DocID"]
    Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
    if Arg1_sent_index - 1 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 1, Arg1_sent_index - 1) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg1_sent_index - 1, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return "%s|%s" % (_list[nearest_item_index][1], _list[nearest_item_index][2])

    if Arg1_sent_index - 2 < 0:
        return "NULL"

    if (DocID, Arg1_sent_index - 2, Arg1_sent_index - 1) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg1_sent_index - 2, Arg1_sent_index - 1)]
        nearest_item_index = 0
        x = -1

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] > x:
                x = conn_indices[-1]
                nearest_item_index = index

        return "%s|%s" % (_list[nearest_item_index][1], _list[nearest_item_index][2])

    return "NULL"

#dict[(DocID, sent1_index, sent2_index)] = [(conn_indices_string, conn, sense)]
def get_next_context_conn(relation, parse_dict, implicit_context_dict):
    DocID = relation["DocID"]
    Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]
    sent_count = len(parse_dict[DocID]["sentences"])

    if Arg2_sent_index + 1 > sent_count - 1:
        return "NULL"

    if (DocID, Arg2_sent_index + 1, Arg2_sent_index + 1) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg2_sent_index + 1, Arg2_sent_index + 1)]
        nearest_item_index = 0
        x = 100

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] < x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][1]

    if Arg2_sent_index + 2 > sent_count - 1:
        return "NULL"

    if (DocID, Arg2_sent_index + 1, Arg2_sent_index + 2) in implicit_context_dict:
        _list = implicit_context_dict[(DocID, Arg2_sent_index + 1, Arg2_sent_index + 2)]
        nearest_item_index = 0
        x = 100

        for index, item in enumerate(_list):
            conn_indices_string, conn, sense = item
            conn_indices = [int(x) for x in conn_indices_string.split(" ")]
            if index == 0:
                x = conn_indices[-1]
            if conn_indices[-1] < x:
                x = conn_indices[-1]
                nearest_item_index = index

        return _list[nearest_item_index][1]

    return "NULL"

#
def get_prev_next_context_conn(relation, parse_dict, implicit_context_dict):
    prev_context_conn = get_prev_context_conn(relation, parse_dict, implicit_context_dict)
    next_context_conn = get_next_context_conn(relation, parse_dict, implicit_context_dict)

    return "%s|%s" % (prev_context_conn, next_context_conn)


if __name__ == "__main__":
    print get_word_MPQA_polarity(('raise', 'verb'))
