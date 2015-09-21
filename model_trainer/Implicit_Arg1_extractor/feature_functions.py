#coding:utf-8
from implicit_arg1_dict import Implicit_arg1_dict
from feature import Feature
import implicit_arg1_dict_util as dict_util
import util

def _all_features(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Implicit_arg1_dict().dict_lowercase_verbs
    dict_lemma_verbs = Implicit_arg1_dict().dict_lemma_verbs
    dict_curr_first = Implicit_arg1_dict().dict_curr_first
    dict_curr_last = Implicit_arg1_dict().dict_curr_last
    dict_prev_last = Implicit_arg1_dict().dict_prev_last
    dict_next_first = Implicit_arg1_dict().dict_next_first
    dict_prev_last_curr_first = Implicit_arg1_dict().dict_prev_last_curr_first
    dict_curr_last_next_first = Implicit_arg1_dict().dict_curr_last_next_first
    dict_position = {"left": 1, "middle": 2, "right": 3}
    dict_prev_curr_CP_production_rule = Implicit_arg1_dict().dict_prev_curr_CP_production_rule
    dict_prev2_pos_lemma_verb = Implicit_arg1_dict().dict_prev2_pos_lemma_verb


    # feature
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)
    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)
    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)
    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)
    prev_last_curr_first = "%s_%s" % (prev_last, curr_first)
    curr_last_next_first = "%s_%s" % (curr_last, next_first)

    # the number of words in curr clause
    clause_word_num = len(arg_clauses.clauses[clause_index][0])
    # the position of current clause
    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)
    # the arg label of current clause

    prev_curr_CP_production_rule = dict_util.get_prev_curr_CP_production_rule(arg_clauses, clause_index, parse_dict)

    prev2_pos_lemma_verb = dict_util.get_2prev_pos_lemma_verb(arg_clauses, clause_index, parse_dict)



    features = []
    features.append(get_feature_by_feat_list(dict_lowercase_verbs, lowercase_verbs_list))
    features.append(get_feature_by_feat_list(dict_lemma_verbs, lemma_verbs_list))

    features.append(get_feature_by_feat(dict_curr_first, curr_first))
    features.append(get_feature_by_feat(dict_curr_last, curr_last))
    features.append(get_feature_by_feat(dict_prev_last, prev_last))
    features.append(get_feature_by_feat(dict_next_first, next_first))
    features.append(get_feature_by_feat(dict_prev_last_curr_first, prev_last_curr_first))
    features.append(get_feature_by_feat(dict_curr_last_next_first, curr_last_next_first))
    features.append(get_feature_by_feat(dict_position, position))
    features.append(Feature("", 1, {"1": clause_word_num}))


    features.append(get_feature_by_feat(dict_prev2_pos_lemma_verb, prev2_pos_lemma_verb))


    ''' production rules '''
    features.append(get_feature_by_feat_list(dict_prev_curr_CP_production_rule, prev_curr_CP_production_rule))


    return util.mergeFeatures(features)

def all_features(arg_clauses, clause_index, parse_dict):

    feature_function_list = [
        prev_curr_CP_production_rule,
        curr_last,
        is_NNP_WP,
        is_curr_NNP_prev_PRP_or_NNP,
        clause_word_num,
        prev2_pos_lemma_verb,
        lemma_verbs
    ]

    features = [feature_function(arg_clauses, clause_index, parse_dict) for feature_function in feature_function_list]
    # merge features
    feature = util.mergeFeatures(features)
    return feature

def lowercase_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Implicit_arg1_dict().dict_lowercase_verbs
    # feature
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lowercase_verbs, lowercase_verbs_list)

def lemma_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lemma_verbs = Implicit_arg1_dict().dict_lemma_verbs
    # feature
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lemma_verbs, lemma_verbs_list)

def curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first = Implicit_arg1_dict().dict_curr_first
    # feature
    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first, curr_first)

def curr_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last = Implicit_arg1_dict().dict_curr_last
    # feature
    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last, curr_last)

def prev_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last = Implicit_arg1_dict().dict_prev_last
    # feature
    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last, prev_last)

def next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_next_first = Implicit_arg1_dict().dict_next_first
    # feature
    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_next_first, next_first)

def prev_last_curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last_curr_first = Implicit_arg1_dict().dict_prev_last_curr_first
    # feature
    prev_last_curr_first = dict_util.get_prev_last_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last_curr_first, prev_last_curr_first)

def curr_last_next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last_next_first = Implicit_arg1_dict().dict_curr_last_next_first
    # feature
    curr_last_next_first = dict_util.get_curr_last_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last_next_first, curr_last_next_first)

def production_rule(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_production_rule = Implicit_arg1_dict().dict_curr_production_rule
    # feature
    production_rule_list = dict_util.get_curr_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_curr_production_rule, production_rule_list)

def position(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_position = {"left": 1, "middle": 2, "right": 3}
    # feature
    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_position, position)

def is_curr_NNP_prev_PRP_or_NNP(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_is_curr_NNP_prev_PRP_or_NNP = {"NONE": 1, "yes": 2, "no": 2}
    # feature
    is_curr_NNP_prev_PRP_or_NNP = dict_util.get_is_curr_NNP_prev_PRP_or_NNP(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_is_curr_NNP_prev_PRP_or_NNP, is_curr_NNP_prev_PRP_or_NNP)

def prev_curr_production_rule(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_curr_production_rule = Implicit_arg1_dict().dict_prev_curr_production_rule
    # feature
    prev_curr_production_rule = dict_util.get_prev_curr_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_prev_curr_production_rule, prev_curr_production_rule)

def prev_curr_CP_production_rule(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_curr_CP_production_rule = Implicit_arg1_dict().dict_prev_curr_CP_production_rule
    # feature
    prev_curr_CP_production_rule = dict_util.get_prev_curr_CP_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_prev_curr_CP_production_rule, prev_curr_CP_production_rule)

def curr_next_CP_production_rule(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_next_CP_production_rule = Implicit_arg1_dict().dict_curr_next_CP_production_rule
    # feature
    curr_next_CP_production_rule = dict_util.get_curr_next_CP_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_curr_next_CP_production_rule, curr_next_CP_production_rule)

def prev2_pos_lemma_verb(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev2_pos_lemma_verb = Implicit_arg1_dict().dict_prev2_pos_lemma_verb
    # feature
    prev2_pos_lemma_verb = dict_util.get_2prev_pos_lemma_verb(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev2_pos_lemma_verb, prev2_pos_lemma_verb)

def curr_first_to_prev_last_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first_to_prev_last_path = Implicit_arg1_dict().dict_curr_first_to_prev_last_path
    # feature
    curr_first_to_prev_last_path = dict_util.get_curr_first_to_prev_last_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first_to_prev_last_path, curr_first_to_prev_last_path)

def clause_word_num(arg_clauses, clause_index, parse_dict):
    # load dict

    # feature
    clause_word_num = len(arg_clauses.clauses[clause_index][0])

    return Feature("", 1, {"1": clause_word_num})

def is_NNP_WP(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_is_NNP_WP = {"NONE": 1, "yes": 2, "no": 3}
    # feature
    is_NNP_WP = dict_util.get_is_NNP_WP(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_is_NNP_WP, is_NNP_WP)





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
