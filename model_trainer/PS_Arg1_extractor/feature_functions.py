#coding:utf-8
from ps_arg1_dict import Ps_arg1_dict
from feature import Feature
import ps_arg1_dict_util as dict_util
import util

def _all_features(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Ps_arg1_dict().dict_lowercase_verbs
    dict_lemma_verbs = Ps_arg1_dict().dict_lemma_verbs
    dict_curr_first = Ps_arg1_dict().dict_curr_first
    dict_curr_last = Ps_arg1_dict().dict_curr_last
    dict_prev_last = Ps_arg1_dict().dict_prev_last
    dict_next_first = Ps_arg1_dict().dict_next_first
    dict_prev_last_curr_first = Ps_arg1_dict().dict_prev_last_curr_first
    dict_curr_last_next_first = Ps_arg1_dict().dict_curr_last_next_first
    dict_curr_production_rule = Ps_arg1_dict().dict_curr_production_rule
    dict_position = {"left": 1, "middle": 2, "right": 3}

    ''' mine '''
    dict_con_str = Ps_arg1_dict().dict_con_str
    dict_con_lstr = Ps_arg1_dict().dict_con_lstr
    dict_con_cat = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }
    dict_conn_to_root_path = Ps_arg1_dict().dict_conn_to_root_path
    dict_conn_to_root_compressed_path = Ps_arg1_dict().dict_conn_to_root_compressed_path
    dict_conn_curr_position = Ps_arg1_dict().dict_conn_curr_position
    dict_is_clause_contain_comma_which = {"YES": 1, "NO": 2}

    # feature
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)
    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)
    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)
    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)
    prev_last_curr_first = dict_util.get_prev_last_curr_first(arg_clauses, clause_index, parse_dict)
    curr_last_next_first = dict_util.get_curr_last_next_first(arg_clauses, clause_index, parse_dict)

    # the position of the current clause
    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)

    production_rule_list = dict_util.get_curr_production_rule(arg_clauses, clause_index, parse_dict)

    ''' mine '''
    con_str = dict_util.get_con_str(arg_clauses, clause_index, parse_dict)
    con_lstr = dict_util.get_con_lstr(arg_clauses, clause_index, parse_dict)
    con_cat = dict_util.get_con_cat(arg_clauses, clause_index, parse_dict)
    conn_to_root_path = dict_util.get_conn_to_root_path(arg_clauses, clause_index, parse_dict)
    conn_to_root_compressed_path = dict_util.get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict)
    conn_curr_position = dict_util.get_conn_curr_position(arg_clauses, clause_index, parse_dict)


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

    ''' production rules '''
    features.append(get_feature_by_feat_list(dict_curr_production_rule, production_rule_list))

    ''' mine '''
    features.append(get_feature_by_feat(dict_con_str, con_str))
    features.append(get_feature_by_feat(dict_con_lstr, con_lstr))
    features.append(get_feature_by_feat(dict_con_cat, con_cat))
    features.append(get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path))
    features.append(get_feature_by_feat(dict_conn_to_root_compressed_path, conn_to_root_compressed_path))
    features.append(get_feature_by_feat(dict_conn_curr_position, conn_curr_position))

    return util.mergeFeatures(features)

def all_features(arg_clauses, clause_index, parse_dict):
    feature_function_list = [
        # lowercase_verbs,
        lemma_verbs,
        curr_first,
        curr_last,
        # prev_last,
        # next_first,
        prev_last_curr_first,
        # curr_last_next_first,
        # production_rule_list,
        # position,
        # # mine
        # con_str,
        con_lstr,
        con_cat,
        # conn_to_root_path,
        # conn_to_root_compressed_path,
        # conn_curr_position
    ]

    features = [feature_function(arg_clauses, clause_index, parse_dict) for feature_function in feature_function_list]
    #合并特征
    feature = util.mergeFeatures(features)
    return feature

def lowercase_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lowercase_verbs = Ps_arg1_dict().dict_lowercase_verbs
    # feature
    lowercase_verbs_list = dict_util.get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lowercase_verbs, lowercase_verbs_list)

def lemma_verbs(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_lemma_verbs = Ps_arg1_dict().dict_lemma_verbs
    # feature
    lemma_verbs_list = dict_util.get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_lemma_verbs, lemma_verbs_list)

def curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first = Ps_arg1_dict().dict_curr_first
    # feature
    curr_first = dict_util.get_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first, curr_first)

def curr_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last = Ps_arg1_dict().dict_curr_last

    curr_last = dict_util.get_curr_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last, curr_last)


def prev_last(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last = Ps_arg1_dict().dict_prev_last

    prev_last = dict_util.get_prev_last(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last, prev_last)

def next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_next_first = Ps_arg1_dict().dict_next_first

    next_first = dict_util.get_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_next_first, next_first)

def prev_last_curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_prev_last_curr_first = Ps_arg1_dict().dict_prev_last_curr_first

    prev_last_curr_first = dict_util.get_prev_last_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_prev_last_curr_first, prev_last_curr_first)


def curr_last_next_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_last_next_first = Ps_arg1_dict().dict_curr_last_next_first

    curr_last_next_first = dict_util.get_curr_last_next_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_last_next_first, curr_last_next_first)

def production_rule_list(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_production_rule = Ps_arg1_dict().dict_curr_production_rule

    production_rule_list = dict_util.get_curr_production_rule(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat_list(dict_curr_production_rule, production_rule_list)

def position(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_position = {"left": 1, "middle": 2, "right": 3}

    position = dict_util.get_curr_position(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_position, position)


def con_str(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_str = Ps_arg1_dict().dict_con_str

    con_str = dict_util.get_con_str(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_str, con_str)

def con_lstr(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_lstr = Ps_arg1_dict().dict_con_lstr

    con_lstr = dict_util.get_con_lstr(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_lstr, con_lstr)

def con_cat(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_con_cat = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }

    con_cat = dict_util.get_con_cat(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_con_cat, con_cat)

def conn_to_root_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_to_root_path = Ps_arg1_dict().dict_conn_to_root_path

    conn_to_root_path = dict_util.get_conn_to_root_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path)

def conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_to_root_compressed_path = Ps_arg1_dict().dict_conn_to_root_compressed_path

    conn_to_root_compressed_path = dict_util.get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_to_root_compressed_path, conn_to_root_compressed_path)

def conn_curr_position(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_curr_position = Ps_arg1_dict().dict_conn_curr_position

    conn_curr_position = dict_util.get_conn_curr_position(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_curr_position, conn_curr_position)


def curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_curr_first_prev_last_parse_path = Ps_arg1_dict().dict_curr_first_prev_last_parse_path
    # feature
    curr_first_prev_last_parse_path = dict_util.get_curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_curr_first_prev_last_parse_path, curr_first_prev_last_parse_path)


def conn_curr_first(arg_clauses, clause_index, parse_dict):
    # load dict
    dict_conn_curr_first = Ps_arg1_dict().dict_conn_curr_first
    # feature
    conn_curr_first = dict_util.get_conn_curr_first(arg_clauses, clause_index, parse_dict)

    return get_feature_by_feat(dict_conn_curr_first, conn_curr_first)

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
