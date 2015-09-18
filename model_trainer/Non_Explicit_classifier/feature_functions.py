#coding:utf-8
from feature import Feature
from util import mergeFeatures
import util
from syntax_tree import Syntax_tree
import non_exp_dict_util as dict_util
from non_explicit_dict import Non_Explicit_dict
import pickle, config, string

def all_features(relation, parse_dict):
    feature_function_list = [
        # word_pairs,
        production_rules, dependency_rules,
        firstlast_first3,
        # polarity,
        modality,
        verbs,
        brown_cluster_pair,
        Inquirer,
        MPQA_polarity,
    ]

    features = [feature_function(relation, parse_dict) for feature_function in feature_function_list]
    #合并特征
    feature = mergeFeatures(features)
    return feature

def word_pairs(relation, parse_dict):
    ''' load dict '''
    dict_word_pairs = Non_Explicit_dict().dict_word_pairs

    ''' feature '''
    word_pairs = dict_util.get_word_pairs(relation, parse_dict)#["a|b", "b|e"]

    return get_feature_by_feat_list(dict_word_pairs, word_pairs)

def cp_production_rules(relation, parse_dict):
    ''' load dict '''
    dict_cp_production_rules = Non_Explicit_dict().cp_production_rules

    ''' feature '''
    cp_production_rules = dict_util.get_cp_production_rules(relation, parse_dict)#["a|b", "b|e"]

    return get_feature_by_feat_list(dict_cp_production_rules, cp_production_rules)

# def production_rules(relation, parse_dict):
#     '''load dict '''
#     dict_production_rules = Non_Explicit_dict().dict_production_rules
#
#     ''' feature '''
#     Arg1_production_rules = dict_util.get_Arg_production_rules(relation, "Arg1", parse_dict)
#     Arg2_production_rules = dict_util.get_Arg_production_rules(relation, "Arg2", parse_dict)
#     Arg1_and_Arg2_production_rules = list(set(Arg1_production_rules) & set(Arg2_production_rules))
#
#     feat_Arg1 = get_feature_by_feat_list(dict_production_rules, Arg1_production_rules)
#     feat_Arg2 = get_feature_by_feat_list(dict_production_rules, Arg2_production_rules)
#     feat_Arg1_and_Arg2 = get_feature_by_feat_list(dict_production_rules, Arg1_and_Arg2_production_rules)
#
#     return util.mergeFeatures([feat_Arg1, feat_Arg2, feat_Arg1_and_Arg2])

def production_rules(relation, parse_dict):
    '''load dict '''
    dict_production_rules = Non_Explicit_dict().dict_production_rules

    ''' feature '''
    Arg1_production_rules = dict_util.get_Arg_production_rules(relation, "Arg1", parse_dict)
    Arg2_production_rules = dict_util.get_Arg_production_rules(relation, "Arg2", parse_dict)
    Arg1_and_Arg2_production_rules = list(set(Arg1_production_rules) & set(Arg2_production_rules))

    Arg1_production_rules = ["Arg1_%s" % rule for rule in Arg1_production_rules]
    Arg2_production_rules = ["Arg2_%s" % rule for rule in Arg2_production_rules]
    Both_production_rules = ["Both_%s" % rule for rule in Arg1_and_Arg2_production_rules]

    rules = Arg1_production_rules + Arg2_production_rules + Both_production_rules

    return get_feature_by_feat_list(dict_production_rules, rules)

# def arg_brown_cluster(relation, parse_dict):
#     # load dict
#     dict_brown_cluster = Non_Explicit_dict().dict_Arg_brown_cluster
#     ''' feature '''
#     Arg1_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg1", parse_dict)
#     Arg2_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg2", parse_dict)
#     Both_brown_cluster = list(set(Arg1_brown_cluster) & set(Arg2_brown_cluster))
#
#     Arg1_brown_cluster = ["Arg1_%s" % x for x in Arg1_brown_cluster]
#     Arg2_brown_cluster = ["Arg2_%s" % x for x in Arg2_brown_cluster]
#     Both_brown_cluster = ["Both_%s" % x for x in Both_brown_cluster]
#
#     cluster = Arg1_brown_cluster + Arg2_brown_cluster + Both_brown_cluster
#
#     return get_feature_by_feat_list(dict_brown_cluster, cluster)

# 跟他论文一样
def arg_brown_cluster(relation, parse_dict):
    # load dict
    dict_brown_cluster = Non_Explicit_dict().dict_Arg_brown_cluster
    ''' feature '''
    Arg1_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg1", parse_dict)
    Arg2_brown_cluster = dict_util.get_Arg_brown_cluster(relation, "Arg2", parse_dict)
    Both_brown_cluster = list(set(Arg1_brown_cluster) & set(Arg2_brown_cluster))

    Arg1_only = list(set(Arg1_brown_cluster) - set(Arg2_brown_cluster))
    Arg2_only = list(set(Arg2_brown_cluster) - set(Arg1_brown_cluster))

    Arg1_brown_cluster = ["Arg1_%s" % x for x in Arg1_only]
    Arg2_brown_cluster = ["Arg2_%s" % x for x in Arg2_only]
    Both_brown_cluster = ["Both_%s" % x for x in Both_brown_cluster]

    cluster = Arg1_brown_cluster + Arg2_brown_cluster + Both_brown_cluster

    return get_feature_by_feat_list(dict_brown_cluster, cluster)


def dependency_rules(relation, parse_dict):
    ''' load dict '''
    dict_dependency_rules = Non_Explicit_dict().dict_dependency_rules

    ''' feature '''
    Arg1_dependency_rules = dict_util.get_Arg_dependency_rules(relation, "Arg1", parse_dict)
    Arg2_dependency_rules = dict_util.get_Arg_dependency_rules(relation, "Arg2", parse_dict)
    Arg1_and_Arg2_dependency_rules = list(set(Arg1_dependency_rules) & set(Arg2_dependency_rules))

    feat_Arg1 = get_feature_by_feat_list(dict_dependency_rules, Arg1_dependency_rules)
    feat_Arg2 = get_feature_by_feat_list(dict_dependency_rules, Arg2_dependency_rules)
    feat_Arg1_and_Arg2 = get_feature_by_feat_list(dict_dependency_rules, Arg1_and_Arg2_dependency_rules)

    return util.mergeFeatures([feat_Arg1, feat_Arg2, feat_Arg1_and_Arg2])

def firstlast_first3(relation, parse_dict):
    # load dict
    dict_Arg1_first = Non_Explicit_dict().dict_Arg1_first
    dict_Arg1_last = Non_Explicit_dict().dict_Arg1_last
    dict_Arg2_first = Non_Explicit_dict().dict_Arg2_first
    dict_Arg2_last = Non_Explicit_dict().dict_Arg2_last
    dict_Arg1_first_Arg2_first = Non_Explicit_dict().dict_Arg1_first_Arg2_first
    dict_Arg1_last_Arg2_last = Non_Explicit_dict().dict_Arg1_last_Arg2_last
    dict_Arg1_first3 = Non_Explicit_dict().dict_Arg1_first3
    dict_Arg2_first3 = Non_Explicit_dict().dict_Arg2_first3

    ''' feature '''
    Arg1_first, Arg1_last, Arg2_first, Arg2_last,\
    Arg1_first_Arg2_first, Arg1_last_Arg2_last,\
    Arg1_first3, Arg2_first3 \
         = dict_util.get_firstlast_first3(relation, parse_dict)

    features = []
    features.append(get_feature_by_feat(dict_Arg1_first,Arg1_first))
    features.append(get_feature_by_feat(dict_Arg1_last,Arg1_last))
    features.append(get_feature_by_feat(dict_Arg2_first,Arg2_first))
    features.append(get_feature_by_feat(dict_Arg2_last,Arg2_last))
    features.append(get_feature_by_feat(dict_Arg1_first_Arg2_first,Arg1_first_Arg2_first))
    features.append(get_feature_by_feat(dict_Arg1_last_Arg2_last,Arg1_last_Arg2_last))
    features.append(get_feature_by_feat(dict_Arg1_first3,Arg1_first3))
    features.append(get_feature_by_feat(dict_Arg2_first3,Arg2_first3))

    return util.mergeFeatures(features)


#polarity
def polarity(relation, parse_dict):
    vec_arg1 = dict_util.get_polarity_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_polarity_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# MPQA polarity
def MPQA_polarity(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# MPQA polarity score
def MPQA_polarity_score(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_score_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_score_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# 不考虑，strong, weak
def MPQA_polarity_no_strong_weak(relation, parse_dict):
    vec_arg1 = dict_util.get_MPQA_polarity_no_strong_weak_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_MPQA_polarity_no_strong_weak_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)

    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

# # modality
# def modality(relation, parse_dict):
#
#     '''feature'''
#     Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
#     Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)
#
#     Arg1_modality_vec = dict_util.get_modality_vec(Arg1_words)
#     Arg2_modality_vec = dict_util.get_modality_vec(Arg2_words)
#     # cp = util.cross_product(Arg1_modality_vec, Arg2_modality_vec)
#
#     features = []
#     # features.append(get_feature_by_list(Arg1_modality_vec))
#     # features.append(get_feature_by_list(Arg2_modality_vec))
#     # features.append(get_feature_by_list(cp))
#     Arg1_feat = 0
#     if sum(Arg1_modality_vec) > 0:
#         Arg1_feat = 1
#
#     Arg2_feat = 0
#     if sum(Arg2_modality_vec) > 0:
#         Arg2_feat = 1
#
#     feat_1 = Feature("", 2, {1:Arg1_feat, 2: Arg2_feat})
#     # 0_0 ,0_1, 1_1,1_0
#     dict = {"0_0": 1, "0_1": 2, "1_0": 3, "1_1": 4}
#     feat_2 = get_feature_by_feat(dict, "%d_%d" % (Arg1_feat, Arg2_feat))
#
#
#     return util.mergeFeatures([feat_1, feat_2])

# modality
def modality(relation, parse_dict):

    '''feature'''
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)

    # 具体的modal
    Arg1_modality_vec = dict_util.get_modality_vec(Arg1_words)
    Arg2_modality_vec = dict_util.get_modality_vec(Arg2_words)
    cp = util.cross_product(Arg1_modality_vec, Arg2_modality_vec)

    # # presence or absence
    # Arg1_has_modal = [0, 0]
    # Arg2_has_modal = [0, 0]
    # if sum(Arg1_modality_vec) > 0:
    #     Arg1_has_modal[1] = 1
    # else:
    #     Arg1_has_modal[0] = 1
    #
    # if sum(Arg2_modality_vec) > 0:
    #     Arg2_has_modal[1] = 1
    # else:
    #     Arg2_has_modal[0] = 1

    # has_cp = util.cross_product(Arg1_has_modal, Arg2_has_modal)

    features = []
    features.append(get_feature_by_list(Arg1_modality_vec))
    features.append(get_feature_by_list(Arg2_modality_vec))
    features.append(get_feature_by_list(cp))

    # features.append(get_feature_by_list(Arg1_has_modal))
    # features.append(get_feature_by_list(Arg2_has_modal))
    # features.append(get_feature_by_list(has_cp))

    return util.mergeFeatures(features)

def verbs(relation, parse_dict):
    #load dict
    dict_verb_classes = Non_Explicit_dict().dict_verb_classes

    '''feature'''
    # 1. the number of pairs of verbs in Arg1 and Arg2 from same verb class
    Arg1_words = dict_util.get_Arg_Words_List(relation, "Arg1", parse_dict)
    Arg2_words = dict_util.get_Arg_Words_List(relation, "Arg2", parse_dict)

    count = 0
    for w1, w2 in [(w1.lower(), w2.lower()) for w1 in Arg1_words for w2 in Arg2_words]:
        if w1 in dict_verb_classes and w2 in dict_verb_classes:
            c1 = dict_verb_classes[w1]
            c2 = dict_verb_classes[w2]
            if set(c1.split("#")) & set(c2.split("#")) != set([]):
                count += 1
    feat_1 = Feature("", 1, {1: count})
    # print feat_1.feat_string

    # # 2. 动词短语的平均长度,int
    # Arg1_average_length_verb_phrase = dict_util.get_Arg_average_length_verb_phrase(relation, "Arg1", parse_dict)
    # Arg2_average_length_verb_phrase = dict_util.get_Arg_average_length_verb_phrase(relation, "Arg2", parse_dict)
    # cp_average_length_verb_phrase = Arg1_average_length_verb_phrase * Arg2_average_length_verb_phrase
    #
    # feat_2 = Feature("", 3, {1:Arg1_average_length_verb_phrase, 2: Arg2_average_length_verb_phrase})
    # # print feat_2.feat_string

    #3. POS of main verb
    Arg1_MV_POS = dict_util.get_main_verb_pos(relation, "Arg1", parse_dict)
    Arg2_MV_POS = dict_util.get_main_verb_pos(relation, "Arg2", parse_dict)

    # cp_MV_POS = util.cross_product(Arg1_MV_POS, Arg2_MV_POS)

    MV_POS_feature_list = Arg1_MV_POS + Arg2_MV_POS

    MV_POS_feature = get_feature_by_list(MV_POS_feature_list)

    # print Arg1_MV_POS_feature.feat_string
    # print Arg2_MV_POS_feature.feat_string

    return util.mergeFeatures([feat_1, MV_POS_feature])


def Inquirer(relation, parse_dict):
    vec_arg1 = dict_util.get_inquirer_vec(relation, "Arg1", parse_dict)
    vec_arg2 = dict_util.get_inquirer_vec(relation, "Arg2", parse_dict)
    cp = util.cross_product(vec_arg1, vec_arg2)
    feature_list = vec_arg1 + vec_arg2 + cp

    return get_feature_by_list(feature_list)

def brown_cluster_pair(relation, parse_dict):
    ''' load dict '''
    dict_word_pairs = Non_Explicit_dict().dict_brown_cluster
    ''' feature '''
    brown_cluster_pairs = dict_util.get_brown_cluster_pairs(relation, parse_dict)

    return get_feature_by_feat_list(dict_word_pairs, brown_cluster_pairs)

#
def money_date_percent(relation, parse_dict):
    Arg1_MDP = _find_Arg_money_date_percent(relation, "Arg1", parse_dict)
    Arg2_MDP = _find_Arg_money_date_percent(relation, "Arg2", parse_dict)
    cp = util.cross_product(Arg1_MDP, Arg2_MDP)

    return get_feature_by_list(Arg1_MDP + Arg2_MDP + cp)

#[0, 1, 2]
def _find_Arg_money_date_percent(relation, Arg, parse_dict):
    MDP = [0] * 2
    ner_tags = dict_util.get_Arg_NER_TAG_List(relation, Arg, parse_dict)
    for tag in ner_tags:
        if tag == "MONEY":
            MDP[0] = 1
        # if tag == "DATE":
        #     MDP[1] = 1
        if tag == "PERCENT":
            MDP[1] = 1
    return MDP

# main verb pair

def main_verb_pair(relation, parse_dict):
    # load dict
    dict_main_verb_pair = Non_Explicit_dict().dict_main_verb_pair
    #feature
    main_verb_pair = dict_util.get_main_verb_pair(relation, parse_dict)

    return get_feature_by_feat(dict_main_verb_pair, main_verb_pair)

''' word embedding '''

def Arg_word2vec(relation, parse_dict):
    ''' load dict '''
    dict_word2vec = Non_Explicit_dict().word2vec_dict

    ''' feature '''
    Arg1_words = dict_util._get_lower_case_lemma_words(relation, "Arg1", parse_dict)
    Arg2_words = dict_util._get_lower_case_lemma_words(relation, "Arg2", parse_dict)

    Arg1_words = list(set(Arg1_words))
    Arg2_words = list(set(Arg2_words))

    Arg1_vec = [0.0] * 300
    Arg1_length = 0
    for word in Arg1_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg1_vec = util.vec_plus_vec(Arg1_vec, vec)
            Arg1_length += 1

    Arg2_vec = [0.0] * 300
    Arg2_length = 0
    for word in Arg2_words:
        if word in dict_word2vec:
            vec = dict_word2vec[word]
            Arg2_vec = util.vec_plus_vec(Arg2_vec, vec)
            Arg2_length += 1

    # 取平均
    if Arg1_length != 0:
        Arg1_vec = [v/Arg1_length for v in Arg1_vec]
    if Arg2_length != 0:
        Arg2_vec = [v/Arg2_length for v in Arg2_vec]

    feat1 = get_feature_by_list(Arg1_vec)
    feat2 = get_feature_by_list(Arg2_vec)

    return util.mergeFeatures([feat1, feat2])




def word2vec_cluster_pair(relation, parse_dict):
    ''' load dict '''
    dict_word2vec_cluster_pairs = Non_Explicit_dict().dict_word2vec_cluster_pairs
    ''' feature '''
    word2vec_cluster_pairs = dict_util.get_word2vec_cluster_pairs(relation, parse_dict)

    return get_feature_by_feat_list(dict_word2vec_cluster_pairs, word2vec_cluster_pairs)


def arg_tense_pair(relation, parse_dict):
    # load dict
    dict_arg_tense_pair = Non_Explicit_dict().dict_arg_tense_pair
    ''' feature '''
    arg_tense_pair = dict_util.get_arg1_arg2_tense_pair(relation, parse_dict)

    return get_feature_by_feat(dict_arg_tense_pair, arg_tense_pair)

def arg1_tense(relation, parse_dict):
    # load dict
    dict_arg1_tense = Non_Explicit_dict().dict_arg1_tense
    ''' feature '''
    arg1_tense = dict_util.get_arg1_tense(relation, parse_dict)

    return get_feature_by_feat(dict_arg1_tense, arg1_tense)

def arg2_tense(relation, parse_dict):
    # load dict
    dict_arg2_tense = Non_Explicit_dict().dict_arg2_tense
    ''' feature '''
    arg2_tense = dict_util.get_arg2_tense(relation, parse_dict)

    return get_feature_by_feat(dict_arg2_tense, arg2_tense)

def arg_first3_conn_pair(relation, parse_dict):
    # load dict
    dict_arg_first3_conn_pair = Non_Explicit_dict().dict_arg_first3_conn_pair
    ''' feature '''
    arg_first3_conn_pair = dict_util.get_arg_first3_conn_pair(relation, parse_dict)

    return get_feature_by_feat(dict_arg_first3_conn_pair, arg_first3_conn_pair)

def arg1_first3_conn(relation, parse_dict):
    # load dict
    dict_arg1_first3_conn = Non_Explicit_dict().dict_arg1_first3_conn
    ''' feature '''
    arg1_first3_conn = dict_util.get_arg1_first3_conn(relation, parse_dict)

    return get_feature_by_feat(dict_arg1_first3_conn, arg1_first3_conn)

def arg2_first3_conn(relation, parse_dict):
    # load dict
    dict_arg2_first3_conn = Non_Explicit_dict().dict_arg2_first3_conn
    ''' feature '''
    arg2_first3_conn = dict_util.get_arg2_first3_conn(relation, parse_dict)

    return get_feature_by_feat(dict_arg2_first3_conn, arg2_first3_conn)


def verb_pair(relation, parse_dict):
    # load dict
    dict_verb_pair = Non_Explicit_dict().dict_verb_pair
    # feature
    verb_pair = dict_util.get_verb_pair(relation, parse_dict)

    return get_feature_by_feat_list(dict_verb_pair, verb_pair)


def prev_context_conn(relation, parse_dict, non_explicit_context_dict):
    # load dict
    dict_prev_context_conn = Non_Explicit_dict().dict_prev_context_conn
    # feature
    prev_context_conn = dict_util.get_prev_context_conn(relation, parse_dict, non_explicit_context_dict)

    return get_feature_by_feat(dict_prev_context_conn, prev_context_conn)

def prev_context_sense(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_context_sense = Non_Explicit_dict().dict_prev_context_sense
    # feature
    prev_context_sense = dict_util.get_prev_context_sense(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_context_sense, prev_context_sense)

def prev_context_conn_sense(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_context_conn_sense = Non_Explicit_dict().dict_prev_context_conn_sense
    # feature
    prev_context_conn_sense = dict_util.get_prev_context_conn_sense(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_context_conn_sense, prev_context_conn_sense)

def next_context_conn(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_next_context_conn = Non_Explicit_dict().dict_next_context_conn
    # feature
    next_context_conn = dict_util.get_next_context_conn(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_next_context_conn, next_context_conn)


def prev_next_context_conn(relation, parse_dict, implicit_context_dict):
    # load dict
    dict_prev_next_context_conn = Non_Explicit_dict().dict_prev_next_context_conn
    # feature
    prev_next_context_conn = dict_util.get_prev_next_context_conn(relation, parse_dict, implicit_context_dict)

    return get_feature_by_feat(dict_prev_next_context_conn, prev_next_context_conn)



# [0, 1, 0, 1]
def get_feature_by_list(list):
    feat_dict = {}
    for index, item in enumerate(list):
        if item != 0:
            feat_dict[index+1] = item
    return Feature("", len(list), feat_dict)


def get_feature_by_feat(dict, feat):
    feat_dict = {}
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_feat_list(dict, feat_list):
    feat_dict = {}
    for feat in feat_list:
        if feat in dict:
            feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)