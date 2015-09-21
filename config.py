#coding:utf-8


# change the the value of the following two variables

# current working directory.
CWD = "/Users/Hunter/Documents/pycharmSpace/conll2015_discourse/"
# mallet bin path
MALLET_PATH = "/Users/Hunter/Documents/conll2015/mallet"





TRAIN = "train"
DEV = "dev"
TEST = "test"

DATA_PATH = CWD + "data/"

# train path
TRAIN_PATH = CWD + "data/conll15-st-03-04-15-train/"
DEV_PATH = CWD + "data/conll15-st-03-04-15-dev/"

'''train & dev raw text'''
RAW_TRAIN_PATH = TRAIN_PATH + "raw/"
RAW_DEV_PATH = DEV_PATH + "raw/"

''' train & dev conll text'''
CONLL_TRAIN_PATH = TRAIN_PATH + "conll_format/"
CONLL_DEV_PATH = DEV_PATH + "conll_format/"

''' train & dev pdtb data '''
# 删除了六个关系
PDTB_TRAIN_PATH = TRAIN_PATH + "pdtb-data.json"
PDTB_DEV_PATH = DEV_PATH + "pdtb-data.json"
# 未删除了六个关系
PDTB_ORIGIN_DEV_PATH = DEV_PATH + "pdtb-data_origin.json"

''' train & dev parsers '''
PARSERS_TRAIN_PATH_JSON = TRAIN_PATH + "pdtb-parses.json"
PARSERS_DEV_PATH_JSON = DEV_PATH + "pdtb-parses.json"

'''Brown cluster '''
# BROWN_CLUSTER_PATH = CWD + "data/brown_cluster_100.txt"
# BROWN_CLUSTER_PATH = CWD + "data/brown_cluster_320.txt"
# BROWN_CLUSTER_PATH = CWD + "data/brown_cluster_1000.txt"
BROWN_CLUSTER_PATH = CWD + "data/brown_cluster_3200.txt"


''' word2vec cluster '''
WORD2VEC_CLUSTER_PATH = CWD + "data/word2vec_cluster"

'''Explicit Connectives'''
ExpConn_PATH = CWD + "data/ExpConn.txt"
SORTED_ExpConn_PATH = CWD + "data/sortedExpConn.txt"

''' dict  文件夹路径 '''
DICT_PATH = CWD + "dict/"

''' connnective dict 路径 '''
CONNECTIVE_DICT_PATH = DICT_PATH + "connective/"
''' connnective dict 路径下 dict的名称 '''
CONNECTIVE_DICT_CPOS_PATH = CONNECTIVE_DICT_PATH + "cpos_dict.txt"
CONNECTIVE_DICT_PREV_C_PATH = CONNECTIVE_DICT_PATH +"prev_c_dict.txt"
CONNECTIVE_DICT_PREVPOS_PATH = CONNECTIVE_DICT_PATH +"prevpos_dict.txt"
CONNECTIVE_DICT_PREVPOS_CPOS_PATH = CONNECTIVE_DICT_PATH + "prevpos_cpos_dict.txt"
CONNECTIVE_DICT_C_NEXT_PATH = CONNECTIVE_DICT_PATH + "c_next_dict.txt"
CONNECTIVE_DICT_NEXTPOS_PATH = CONNECTIVE_DICT_PATH + "nextpos_dict.txt"
CONNECTIVE_DICT_CPOS_NEXTPOS_PATH = CONNECTIVE_DICT_PATH + "cpos_nextpos_dict.txt"
CONNECTIVE_DICT_CPARENT_TO_ROOT_PATH = CONNECTIVE_DICT_PATH+ "cparent_to_root_path_dict.txt"
CONNECTIVE_DICT_COMPRESSED_CPARENT_TO_ROOT_PATH = CONNECTIVE_DICT_PATH+ "compressed_cparent_to_root_path_dict.txt"

#pitler
CONNECTIVE_DICT_SELF_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "self_category_dict.txt"
CONNECTIVE_DICT_PARENT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "parent_category_dict.txt"
CONNECTIVE_DICT_LEFT_SIBLING_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "left_sibling_category_dict.txt"
CONNECTIVE_DICT_RIGHT_SIBLING_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "right_sibling_category_dict.txt"

#pitler , conn syn interaction
CONNECTIVE_DICT_CONN_SELF_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "conn_self_category_dict.txt"
CONNECTIVE_DICT_CONN_PARENT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "conn_parent_category_dict.txt"
CONNECTIVE_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "conn_left_sibling_category_dict.txt"
CONNECTIVE_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "conn_right_sibling_category_dict.txt"
#pitler , syn syn interaction
CONNECTIVE_DICT_SELF_PARENT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "self_parent_dict.txt"
CONNECTIVE_DICT_SELF_RIGHT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "self_right_dict.txt"
CONNECTIVE_DICT_SELF_LEFT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "self_left_dict.txt"
CONNECTIVE_DICT_PARENT_LEFT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "parent_left_dict.txt"
CONNECTIVE_DICT_PARENT_RIGHT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "parent_right_dict.txt"
CONNECTIVE_DICT_LEFT_RIGHT_CATEGORY_PATH = CONNECTIVE_DICT_PATH + "left_right_dict.txt"

# mine
CONNECTIVE_DICT_CONN_LOWER_CASE = CONNECTIVE_DICT_PATH + "conn_lower_case_dict.txt"
CONNECTIVE_DICT_CONN = CONNECTIVE_DICT_PATH + "conn.txt"
CONNECTIVE_DICT_PREVPOS_C = CONNECTIVE_DICT_PATH + "prevPOS_C.txt"
CONNECTIVE_DICT_SELF_CATEGORY_TO_ROOT_PATH = CONNECTIVE_DICT_PATH + "self_category_to_root_path.txt"
CONNECTIVE_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES = CONNECTIVE_DICT_PATH + "CParent_to_root_path_node_names_dict.txt"
CONNECTIVE_DICT_CONN_CONNCTX = CONNECTIVE_DICT_PATH + "conn_connCtx.txt"
CONNECTIVE_DICT_CONN_RIGHTSIBLINGCTX = CONNECTIVE_DICT_PATH + "conn_rightsiblingCtx.txt"
CONNECTIVE_DICT_CONN_LEFTSIBLINGCTX = CONNECTIVE_DICT_PATH + "conn_leftsiblingCtx.txt"
CONNECTIVE_DICT_CONN_LEFT_RIGHT_SIBLINGCTX = CONNECTIVE_DICT_PATH + "conn_left_right_siblingCtx.txt"
CONNECTIVE_DICT_CONN_PARENT_CATEGORY_CTX = CONNECTIVE_DICT_PATH + "conn_parent_category_Ctx.txt"
CONNECTIVE_DICT_CONN_RIGHTSIBLING_PRODUCTION_RULES = CONNECTIVE_DICT_PATH + "rightSibling_production_rules.txt"







''' argument position dict '''
ARG_POSITION_DICT_PATH = DICT_PATH + "argument_position/"
''' argument position dict 路径下 dict的名称 '''
ARG_POSITION_DICT_CSTRING = ARG_POSITION_DICT_PATH + "ctring_dict.txt"
ARG_POSITION_DICT_CPOS = ARG_POSITION_DICT_PATH + "cpos_dict.txt"
ARG_POSITION_DICT_PREV1 = ARG_POSITION_DICT_PATH + "prev1_dict.txt"
ARG_POSITION_DICT_PREV1POS = ARG_POSITION_DICT_PATH + "prev1pos_dict.txt"
ARG_POSITION_DICT_PREV1_C = ARG_POSITION_DICT_PATH + "prev1_C_dict.txt"
ARG_POSITION_DICT_PREV1POS_CPOS = ARG_POSITION_DICT_PATH + "prev1pos_Cpos_dict.txt"
ARG_POSITION_DICT_PREV2 = ARG_POSITION_DICT_PATH + "prev2_dict.txt"
ARG_POSITION_DICT_PREV2POS = ARG_POSITION_DICT_PATH + "prev2pos_dict.txt"
ARG_POSITION_DICT_PREV2_C = ARG_POSITION_DICT_PATH + "prev2_C_dict.txt"
ARG_POSITION_DICT_PREV2POS_CPOS = ARG_POSITION_DICT_PATH + "prev2pos_Cpos_dict.txt"

ARG_POSITION_DICT_NEXT1 = ARG_POSITION_DICT_PATH + "next1_dict.txt"
ARG_POSITION_DICT_NEXT1POS = ARG_POSITION_DICT_PATH + "next1pos_dict.txt"
ARG_POSITION_DICT_NEXT1_C = ARG_POSITION_DICT_PATH + "next1_C_dict.txt"
ARG_POSITION_DICT_NEXT1POS_CPOS = ARG_POSITION_DICT_PATH + "next1pos_Cpos_dict.txt"
ARG_POSITION_DICT_NEXT2 = ARG_POSITION_DICT_PATH + "next2_dict.txt"
ARG_POSITION_DICT_NEXT2POS = ARG_POSITION_DICT_PATH + "next2pos_dict.txt"
ARG_POSITION_DICT_NEXT2_C = ARG_POSITION_DICT_PATH + "next2_C_dict.txt"
ARG_POSITION_DICT_NEXT2POS_CPOS = ARG_POSITION_DICT_PATH + "next2pos_Cpos_dict.txt"

ARG_POSITION_DICT_CONN_TO_ROOT_PATH = ARG_POSITION_DICT_PATH + "conn_to_root_path.txt"



''' constituent-based '''
NT_DICT = DICT_PATH + "NT/"
NT_DICT_CON_Str = NT_DICT + "con_str.txt"
NT_DICT_CON_LStr = NT_DICT + "con_lstr.txt"
NT_DICT_NT_Ctx = NT_DICT + "nt_ctx.txt"
NT_DICT_CON_NT_Path = NT_DICT + "con_nt_path.txt"
NT_DICT_CON_NT_Path_iLsib = NT_DICT + "con_nt_path_ilsib.txt"

NT_DICT_PREV_CURR_PATH = NT_DICT + "nt_prev_curr_path.txt"
NT_DICT_CON_POS = NT_DICT + "con_pos.txt"
NT_DICT_C_PREV = NT_DICT + "c_prev.txt"
NT_DICT_NT_NAME = NT_DICT + "nt_name.txt"
NT_DICT_NT_PREV_CURR_PRODUCTION_RULE = NT_DICT + "nt_prev_curr_production_rule.txt"

''' mine '''
NT_DICT_NT_NTPARENT_CTX = NT_DICT + "nt_ntParent_ctx.txt"
NT_DICT_CPARENT_TO_ROOT_PATH = NT_DICT + "cparent_to_root_path.txt"

# conn
NT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES = NT_DICT + "CParent_to_root_path_node_names.txt"
NT_DICT_CONN_CONNCTX = NT_DICT + "conn_connCtx.txt"
NT_DICT_CONN_PARENT_CATEGORYCTX = NT_DICT + "conn_parent_categoryCtx.txt"
NT_DICT_CONN_RIGHTSIBLINGCTX = NT_DICT + "conn_rightSiblingCtx.txt"
NT_DICT_SELF_CATEGORY = NT_DICT + "self_category.txt"
NT_DICT_PARENT_CATEGORY = NT_DICT + "parent_category.txt"
NT_DICT_LEFT_SIBLING_CATEGORY = NT_DICT + "left_sibling_category.txt"
NT_DICT_RIGHT_SIBLING_CATEGORY = NT_DICT + "right_sibling_category.txt"

# NT
NT_DICT_NT_LINKED_CTX = NT_DICT + "NT_Linked_ctx.txt"
NT_DICT_NT_TO_ROOT_PATH = NT_DICT + "NT_to_root_path.txt"
NT_DICT_NT_PARENT_LINKED_CTX = NT_DICT + "NT_parent_linked_ctx.txt"








''' explicit classifier '''
EXPLICIT_DICT = DICT_PATH + "explicit_classifier/"
EXPLICIT_DICT_CSTRING = EXPLICIT_DICT + "cstring.txt"
EXPLICIT_DICT_CPOS = EXPLICIT_DICT + "cpos.txt"
EXPLICIT_DICT_C_PREV = EXPLICIT_DICT + "c_prev.txt"

EXPLICIT_DICT_CLSTRING = EXPLICIT_DICT + "clstring.txt"

#pitler
EXPLICIT_DICT_SELF_CATEGORY_PATH = EXPLICIT_DICT + "self_category_dict.txt"
EXPLICIT_DICT_PARENT_CATEGORY_PATH = EXPLICIT_DICT + "parent_category_dict.txt"
EXPLICIT_DICT_LEFT_SIBLING_CATEGORY_PATH = EXPLICIT_DICT + "left_sibling_category_dict.txt"
EXPLICIT_DICT_RIGHT_SIBLING_CATEGORY_PATH = EXPLICIT_DICT + "right_sibling_category_dict.txt"

#pitler , conn syn interaction
EXPLICIT_DICT_CONN_SELF_CATEGORY_PATH = EXPLICIT_DICT + "conn_self_category_dict.txt"
EXPLICIT_DICT_CONN_PARENT_CATEGORY_PATH = EXPLICIT_DICT + "conn_parent_category_dict.txt"
EXPLICIT_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH = EXPLICIT_DICT + "conn_left_sibling_category_dict.txt"
EXPLICIT_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH = EXPLICIT_DICT + "conn_right_sibling_category_dict.txt"
# pitler , syn- syn
EXPLICIT_DICT_SELF_PARENT_CATEGORY_PATH = EXPLICIT_DICT + "self_parent_dict.txt"
EXPLICIT_DICT_SELF_RIGHT_CATEGORY_PATH = EXPLICIT_DICT + "self_right_dict.txt"
EXPLICIT_DICT_SELF_LEFT_CATEGORY_PATH = EXPLICIT_DICT + "self_left_dict.txt"
EXPLICIT_DICT_PARENT_LEFT_CATEGORY_PATH = EXPLICIT_DICT + "parent_left_dict.txt"
EXPLICIT_DICT_PARENT_RIGHT_CATEGORY_PATH = EXPLICIT_DICT + "parent_right_dict.txt"
EXPLICIT_DICT_LEFT_RIGHT_CATEGORY_PATH = EXPLICIT_DICT + "left_right_dict.txt"
# mine
EXPLICIT_DICT_CONN_TO_ROOT_PATH = EXPLICIT_DICT + "conn_to_root_path.txt"
EXPLICIT_DICT_CONN_NEXT = EXPLICIT_DICT + "conn_next.txt"
EXPLICIT_DICT_CONN_CONNCTX = EXPLICIT_DICT + "conn_connCtx.txt"
EXPLICIT_DICT_CONN_RIGHTSIBLINGCTX = EXPLICIT_DICT + "conn_rightSiblingCtx.txt"
EXPLICIT_DICT_CONN_PARENT_CATEGORY_CTX = EXPLICIT_DICT + "conn_parent_category_Ctx.txt"
EXPLICIT_DICT_CONN_LEFTSIBLING_CTX = EXPLICIT_DICT + "conn_leftSibling_ctx.txt"
EXPLICIT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES = EXPLICIT_DICT + "CParent_to_root_path_node_names.txt"
EXPLICIT_DICT_CONN_PARENT_CATEGORY_NOT_LINKED_CTX = EXPLICIT_DICT + "conn_parent_category_not_linked_Ctx.txt"
EXPLICIT_DICT_CONN_PREV_CONN = EXPLICIT_DICT + "conn_prev_conn.txt"
EXPLICIT_DICT_PREV_CONN = EXPLICIT_DICT + "prev_conn.txt"
EXPLICIT_DICT_AS_PREV_CONN = EXPLICIT_DICT + "as_prev_conn.txt"
EXPLICIT_DICT_AS_PREV_CONNPOS = EXPLICIT_DICT + "as_prev_connPOS.txt"
EXPLICIT_DICT_WHEN_PREV_CONN = EXPLICIT_DICT + "when_prev_conn.txt"
EXPLICIT_DICT_WHEN_PREV_CONNPOS = EXPLICIT_DICT + "when_prev_connPOS.txt"

EXPLICIT_DICT_AS_BEFORE_AFTER_TENSE = EXPLICIT_DICT + "as_before_after_tense.txt"
EXPLICIT_DICT_WHEN_BEFORE_AFTER_TENSE = EXPLICIT_DICT + "when_before_after_tense.txt"
EXPLICIT_DICT_WHEN_AFTER_LEMMA_VERBS = EXPLICIT_DICT + "when_after_lemma_verbs.txt"





''' Non-Explicit Dict '''
NON_EXPLICIT_DICT = DICT_PATH + "non_explicit_classifier/"
NON_EXPLICIT_DICT_WORD_PAIRS = NON_EXPLICIT_DICT + "word_pairs.txt"
NON_EXPLICIT_DICT_PRODUCTION_RULES = NON_EXPLICIT_DICT + "production_rules.txt"
NON_EXPLICIT_DICT_DEPENDENCY_RULES = NON_EXPLICIT_DICT + "dependency_rules.txt"
# firstlast,first3
NON_EXPLICIT_DICT_Arg1_first = NON_EXPLICIT_DICT + "Arg1_first.txt"
NON_EXPLICIT_DICT_Arg1_last = NON_EXPLICIT_DICT + "Arg1_last.txt"
NON_EXPLICIT_DICT_Arg2_first = NON_EXPLICIT_DICT + "Arg2_first.txt"
NON_EXPLICIT_DICT_Arg2_last = NON_EXPLICIT_DICT + "Arg2_last.txt"
NON_EXPLICIT_DICT_Arg1_first_Arg2_first = NON_EXPLICIT_DICT + "Arg1_first_Arg2_first.txt"
NON_EXPLICIT_DICT_Arg1_last_Arg2_last = NON_EXPLICIT_DICT + "Arg1_last_Arg2_last.txt"
NON_EXPLICIT_DICT_Arg1_first3 = NON_EXPLICIT_DICT + "Arg1_first3.txt"
NON_EXPLICIT_DICT_Arg2_first3 = NON_EXPLICIT_DICT + "Arg2_first3.txt"
# brown
NON_EXPLICIT_DICT_BROWN_CLUSTER_PAIRS = NON_EXPLICIT_DICT + "brown_cluster_pairs.txt"
# all words
NON_EXPLICIT_DICT_ALL_WORDS = NON_EXPLICIT_DICT + "all_words.txt"
# lemma word
NON_EXPLICIT_DICT_LOWER_CASE_LEMMA_WORDS = NON_EXPLICIT_DICT + "lower_case_lemma_words.txt"
# word2vec
NON_EXPLICIT_DICT_WORD2VEC =  NON_EXPLICIT_DICT + "word2vec.txt"
# main verb pair
NON_EXPLICIT_DICT_MAIN_VERB_PAIR = NON_EXPLICIT_DICT + "main_verb_pair.txt"
# cp production rule
NON_EXPLICIT_DICT_CP_PRODUCTION_RULES = NON_EXPLICIT_DICT + "cp_production_rules.txt"
# arg1 arg2 tense pair
NON_EXPLICIT_DICT_ARG1_TENSE = NON_EXPLICIT_DICT + "arg1_tense.txt"
NON_EXPLICIT_DICT_ARG2_TENSE = NON_EXPLICIT_DICT + "arg2_tense.txt"
NON_EXPLICIT_DICT_ARG_TENSE_PAIR = NON_EXPLICIT_DICT + "arg_tense_pair.txt"
# arg first conn
NON_EXPLICIT_DICT_ARG1_FIRST3_CONN = NON_EXPLICIT_DICT + "arg1_first3_conn.txt"
NON_EXPLICIT_DICT_ARG2_FIRST3_CONN = NON_EXPLICIT_DICT + "arg2_first3_conn.txt"
NON_EXPLICIT_DICT_ARG_FIRST3_CONN_PAIR = NON_EXPLICIT_DICT + "arg_first3_conn_pair.txt"
# verb pair
NON_EXPLICIT_DICT_VERB_PAIR = NON_EXPLICIT_DICT + "verb_pair.txt"
# brown cluster
NON_EXPLICIT_DICT_ARG_BROWN_CLUSTER = NON_EXPLICIT_DICT + "arg_brown_cluster.txt"
# context
NON_EXPLICIT_DICT_PREV_CONTEXT_CONN = NON_EXPLICIT_DICT + "prev_context_conn.txt"
NON_EXPLICIT_DICT_PREV_CONTEXT_SENSE = NON_EXPLICIT_DICT + "prev_context_sense.txt"
NON_EXPLICIT_DICT_PREV_CONTEXT_CONN_SENSE = NON_EXPLICIT_DICT + "prev_context_conn_sense.txt"

NON_EXPLICIT_DICT_NEXT_CONTEXT_CONN = NON_EXPLICIT_DICT + "next_context_conn.txt"

NON_EXPLICIT_DICT_PREV_NEXT_CONTEXT_CONN = NON_EXPLICIT_DICT + "prev_next_context_conn.txt"

''' Attribution Span Labler '''
''' NON_CONNS_DICT '''
ATTRIBUTION_NON_CONNS_DICT = DICT_PATH + "attribution_non_conns/"
ATTRIBUTION_NON_CONNS_DICT_LOWERCASE_VERBS = ATTRIBUTION_NON_CONNS_DICT + "lowercase_verbs.txt"
ATTRIBUTION_NON_CONNS_DICT_LEMMA_VERBS = ATTRIBUTION_NON_CONNS_DICT + "lemma_verbs.txt"

ATTRIBUTION_NON_CONNS_DICT_CURR_FIRST = ATTRIBUTION_NON_CONNS_DICT + "curr_first.txt"
ATTRIBUTION_NON_CONNS_DICT_CURR_LAST = ATTRIBUTION_NON_CONNS_DICT + "curr_last.txt"
ATTRIBUTION_NON_CONNS_DICT_PREV_LAST = ATTRIBUTION_NON_CONNS_DICT + "prev_last.txt"
ATTRIBUTION_NON_CONNS_DICT_NEXT_FIRST = ATTRIBUTION_NON_CONNS_DICT + "next_first.txt"
ATTRIBUTION_NON_CONNS_DICT_PREV_LAST_CURR_FIRST = ATTRIBUTION_NON_CONNS_DICT + "prev_last_curr_first.txt"
ATTRIBUTION_NON_CONNS_DICT_CURR_LAST_NEXT_FIRST = ATTRIBUTION_NON_CONNS_DICT + "curr_last_next_first.txt"
ATTRIBUTION_NON_CONNS_DICT_CURR_PRODUCTION_RULE = ATTRIBUTION_NON_CONNS_DICT + "curr_production_rule.txt"
ATTRIBUTION_NON_CONNS_DICT_PREV_CURR_PRODUCTION_RULE = ATTRIBUTION_NON_CONNS_DICT + "prev_curr_production_rule.txt"
ATTRIBUTION_NON_CONNS_DICT_PREV_CURR_CP_PRODUCTION_RULE = ATTRIBUTION_NON_CONNS_DICT + "prev_curr_CP_production_rule.txt"
ATTRIBUTION_NON_CONNS_DICT_CURR_NEXT_CP_PRODUCTION_RULE = ATTRIBUTION_NON_CONNS_DICT + "curr_next_CP_production_rule.txt"
ATTRIBUTION_NON_CONNS_DICT_2PREV_POS_LEMMA_VERB = ATTRIBUTION_NON_CONNS_DICT + "2prev_pos_lemma_verb.txt"
ATTRIBUTION_NON_CONNS_DICT_CURR_FIRST_TO_PREV_LAST_PATH = ATTRIBUTION_NON_CONNS_DICT + "curr_first_to_prev_last_path.txt"


''' PS Arg2 dict '''

PS_ARG2_DICT = DICT_PATH + "ps_arg2/"
PS_ARG2_DICT_LOWERCASE_VERBS = PS_ARG2_DICT + "lowercase_verbs.txt"
PS_ARG2_DICT_LEMMA_VERBS = PS_ARG2_DICT + "lemma_verbs.txt"

PS_ARG2_DICT_FIRST_LOWERCASE_VERB = PS_ARG2_DICT + "first_lowercase_verb.txt"
PS_ARG2_DICT_FIRST_LEMMA_VERB = PS_ARG2_DICT + "first_lemma_verb.txt"

PS_ARG2_DICT_CURR_FIRST = PS_ARG2_DICT + "curr_first.txt"
PS_ARG2_DICT_CURR_LAST = PS_ARG2_DICT + "curr_last.txt"
PS_ARG2_DICT_PREV_LAST = PS_ARG2_DICT + "prev_last.txt"
PS_ARG2_DICT_NEXT_FIRST = PS_ARG2_DICT + "next_first.txt"
PS_ARG2_DICT_PREV_LAST_CURR_FIRST = PS_ARG2_DICT + "prev_last_curr_first.txt"
PS_ARG2_DICT_CURR_LAST_NEXT_FIRST = PS_ARG2_DICT + "curr_last_next_first.txt"
PS_ARG2_DICT_CURR_PRODUCTION_RULE = PS_ARG2_DICT + "curr_production_rule.txt"
# conn
PS_ARG2_DICT_CONN_STR = PS_ARG2_DICT + "conn_str.txt"
PS_ARG2_DICT_CONN_LSTR = PS_ARG2_DICT + "conn_lstr.txt"
PS_ARG2_DICT_CONN_POSITION_DISTANCE = PS_ARG2_DICT + "conn_position_distance.txt"
PS_ARG2_DICT_CONN_TO_ROOT_PATH = PS_ARG2_DICT + "conn_to_root_path.txt"
PS_ARG2_DICT_CONN_TO_ROOT_COMPRESSED_PATH = PS_ARG2_DICT + "conn_to_root_compressed_path.txt"
PS_ARG2_DICT_CONN_POSITION = PS_ARG2_DICT + "conn_position.txt"
PS_ARG2_DICT_CONN_IS_ADJACENT_TO_CONN = PS_ARG2_DICT + "conn_is_adjacent_to_conn.txt"
PS_ARG2_DICT_CURR_FIRST_CURR_FIRST_LEMMA_VERB = PS_ARG2_DICT + "curr_first_curr_first_lemma_verb.txt"


PS_ARG2_DICT_PREV_CURR_CP_PRODUCTION_RULE = PS_ARG2_DICT + "prev_curr_CP_production_rule.txt"

PS_ARG2_DICT_CURR_FIRST_PREV_LAST_PARSE_PATH = PS_ARG2_DICT + "curr_first_prev_last_parse_path.txt"

PS_ARG2_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES = PS_ARG2_DICT + "CParent_to_root_path_node_names.txt"
PS_ARG2_DICT_CPOS = PS_ARG2_DICT + "CPOS.txt"
PS_ARG2_DICT_CONN_CONNCTX = PS_ARG2_DICT + "conn_connCtx.txt"
PS_ARG2_DICT_CONN_PARENT_CATEGORY_CTX = PS_ARG2_DICT + "curr_first_prev_last_parse_path.txt"
PS_ARG2_DICT_CONN_CURR_FIRST = PS_ARG2_DICT + "conn_curr_first.txt"


''' PS Arg1 dict '''

PS_ARG1_DICT = DICT_PATH + "ps_arg1/"
PS_ARG1_DICT_LOWERCASE_VERBS = PS_ARG1_DICT + "lowercase_verbs.txt"
PS_ARG1_DICT_LEMMA_VERBS = PS_ARG1_DICT + "lemma_verbs.txt"

PS_ARG1_DICT_CURR_FIRST = PS_ARG1_DICT + "curr_first.txt"
PS_ARG1_DICT_CURR_LAST = PS_ARG1_DICT + "curr_last.txt"
PS_ARG1_DICT_PREV_LAST = PS_ARG1_DICT + "prev_last.txt"
PS_ARG1_DICT_NEXT_FIRST = PS_ARG1_DICT + "next_first.txt"
PS_ARG1_DICT_PREV_LAST_CURR_FIRST = PS_ARG1_DICT + "prev_last_curr_first.txt"
PS_ARG1_DICT_CURR_LAST_NEXT_FIRST = PS_ARG1_DICT + "curr_last_next_first.txt"
PS_ARG1_DICT_CURR_PRODUCTION_RULE = PS_ARG1_DICT + "curr_production_rule.txt"
# conn
PS_ARG1_DICT_CONN_STR = PS_ARG1_DICT + "conn_str.txt"
PS_ARG1_DICT_CONN_LSTR = PS_ARG1_DICT + "conn_lstr.txt"
PS_ARG1_DICT_CONN_POSITION_DISTANCE = PS_ARG1_DICT + "conn_position_distance.txt"
PS_ARG1_DICT_CONN_TO_ROOT_PATH = PS_ARG1_DICT + "conn_to_root_path.txt"
PS_ARG1_DICT_CONN_TO_ROOT_COMPRESSED_PATH = PS_ARG1_DICT + "conn_to_root_compressed_path.txt"
PS_ARG1_DICT_CONN_POSITION = PS_ARG1_DICT + "conn_position.txt"
PS_ARG1_DICT_CONN_IS_ADJACENT_TO_CONN = PS_ARG1_DICT + "conn_is_adjacent_to_conn.txt"
PS_ARG1_DICT_CURR_FIRST_CURR_FIRST_LEMMA_VERB = PS_ARG1_DICT + "curr_first_curr_first_lemma_verb.txt"

PS_ARG1_DICT_CONN_CURR_POSITION = PS_ARG1_DICT + "conn_curr_position.txt"

PS_ARG1_DICT_CURR_FIRST_PREV_LAST_PARSE_PATH = PS_ARG1_DICT + "curr_first_prev_last_parse_path.txt"
PS_ARG1_DICT_CONN_CURR_FIRST = PS_ARG1_DICT + "conn_curr_first.txt"

PS_ARG1_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES = PS_ARG1_DICT + "CParent_to_root_path_node_names.txt"
PS_ARG1_DICT_CPOS = PS_ARG1_DICT + "CPOS.txt"
PS_ARG1_DICT_CONN_CONNCTX = PS_ARG1_DICT + "conn_connCtx.txt"
PS_ARG1_DICT_CONN_PARENT_CATEGORY_CTX = PS_ARG1_DICT + "curr_first_prev_last_parse_path.txt"

PS_ARG1_DICT_CLAUSE_FIRST_CONN_POS = PS_ARG1_DICT + "clause_first_conn_pos.txt"
PS_ARG1_DICT_CLAUSE_MAIN_VERB_CONN = PS_ARG1_DICT + "clause_main_verb_conn.txt"


''' Implicit Arg1 '''
IMPLICIT_ARG1_DICT = DICT_PATH + "implicit_arg1/"
IMPLICIT_ARG1_DICT_LOWERCASE_VERBS = IMPLICIT_ARG1_DICT + "lowercase_verbs.txt"
IMPLICIT_ARG1_DICT_LEMMA_VERBS = IMPLICIT_ARG1_DICT + "lemma_verbs.txt"

IMPLICIT_ARG1_DICT_CURR_FIRST = IMPLICIT_ARG1_DICT + "curr_first.txt"
IMPLICIT_ARG1_DICT_CURR_LAST = IMPLICIT_ARG1_DICT + "curr_last.txt"
IMPLICIT_ARG1_DICT_PREV_LAST = IMPLICIT_ARG1_DICT + "prev_last.txt"
IMPLICIT_ARG1_DICT_NEXT_FIRST = IMPLICIT_ARG1_DICT + "next_first.txt"
IMPLICIT_ARG1_DICT_PREV_LAST_CURR_FIRST = IMPLICIT_ARG1_DICT + "prev_last_curr_first.txt"
IMPLICIT_ARG1_DICT_CURR_LAST_NEXT_FIRST = IMPLICIT_ARG1_DICT + "curr_last_next_first.txt"
IMPLICIT_ARG1_DICT_CURR_PRODUCTION_RULE = IMPLICIT_ARG1_DICT + "curr_production_rule.txt"
IMPLICIT_ARG1_DICT_PREV_CURR_PRODUCTION_RULE = IMPLICIT_ARG1_DICT + "prev_curr_production_rule.txt"
IMPLICIT_ARG1_DICT_PREV_CURR_CP_PRODUCTION_RULE = IMPLICIT_ARG1_DICT + "prev_curr_CP_production_rule.txt"
IMPLICIT_ARG1_DICT_CURR_NEXT_CP_PRODUCTION_RULE = IMPLICIT_ARG1_DICT + "curr_next_CP_production_rule.txt"
IMPLICIT_ARG1_DICT_2PREV_POS_LEMMA_VERB = IMPLICIT_ARG1_DICT + "2prev_pos_lemma_verb.txt"
IMPLICIT_ARG1_DICT_CURR_FIRST_TO_PREV_LAST_PATH = IMPLICIT_ARG1_DICT + "curr_first_to_prev_last_path.txt"

''' Implicit Arg2 '''
IMPLICIT_ARG2_DICT = DICT_PATH + "implicit_arg2/"
IMPLICIT_ARG2_DICT_LOWERCASE_VERBS = IMPLICIT_ARG2_DICT + "lowercase_verbs.txt"
IMPLICIT_ARG2_DICT_LEMMA_VERBS = IMPLICIT_ARG2_DICT + "lemma_verbs.txt"

IMPLICIT_ARG2_DICT_CURR_FIRST = IMPLICIT_ARG2_DICT + "curr_first.txt"
IMPLICIT_ARG2_DICT_CURR_LAST = IMPLICIT_ARG2_DICT + "curr_last.txt"
IMPLICIT_ARG2_DICT_PREV_LAST = IMPLICIT_ARG2_DICT + "prev_last.txt"
IMPLICIT_ARG2_DICT_NEXT_FIRST = IMPLICIT_ARG2_DICT + "next_first.txt"
IMPLICIT_ARG2_DICT_PREV_LAST_CURR_FIRST = IMPLICIT_ARG2_DICT + "prev_last_curr_first.txt"
IMPLICIT_ARG2_DICT_CURR_LAST_NEXT_FIRST = IMPLICIT_ARG2_DICT + "curr_last_next_first.txt"
IMPLICIT_ARG2_DICT_CURR_PRODUCTION_RULE = IMPLICIT_ARG2_DICT + "curr_production_rule.txt"
IMPLICIT_ARG2_DICT_PREV_CURR_PRODUCTION_RULE = IMPLICIT_ARG2_DICT + "prev_curr_production_rule.txt"
IMPLICIT_ARG2_DICT_PREV_CURR_CP_PRODUCTION_RULE = IMPLICIT_ARG2_DICT + "prev_curr_CP_production_rule.txt"
IMPLICIT_ARG2_DICT_CURR_NEXT_CP_PRODUCTION_RULE = IMPLICIT_ARG2_DICT + "curr_next_CP_production_rule.txt"
IMPLICIT_ARG2_DICT_2PREV_POS_LEMMA_VERB = IMPLICIT_ARG2_DICT + "2prev_pos_lemma_verb.txt"
IMPLICIT_ARG2_DICT_CURR_FIRST_TO_PREV_LAST_PATH = IMPLICIT_ARG2_DICT + "curr_first_to_prev_last_path.txt"


''' 使用pickle 保存的 dict '''
PICKLE_PATH = DICT_PATH + "pickle/"
PICKLE_DISC_CONNS_PATH = PICKLE_PATH+"disc_conns.p"
PICKLE_NON_DISC_CONNS_PATH = PICKLE_PATH+"non_disc_conns.p"
PICKLE_POLARITY_PATH = PICKLE_PATH+"polairty.p"


FEATURE_OUTPUT_PATH = CWD + "model_trainer/feature_output/"
''' connective 的特征文件路径 '''
#feature output
CONNECTIVE_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "connective_train_feature.txt"
CONNECTIVE_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "connective_dev_feature.txt"

ARG_POSITION_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "arg_position_train_feature.txt"
ARG_POSITION_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "arg_position_dev_feature.txt"

ARG_EXTRACTOR_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "arg_extractor_train_feature.txt"
ARG_EXTRACTOR_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "arg_extractor_dev_feature.txt"

NT_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "nt_train_feature.txt"
NT_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "nt_dev_feature.txt"

EXPLICIT_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "explicit_train_feature.txt"
EXPLICIT_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "explicit_dev_feature.txt"

NON_EXPLICIT_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "non_explicit_train_feature.txt"
NON_EXPLICIT_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "non_explicit_dev_feature.txt"

ATTRI_NON_CONNS_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "attri_non_conns_train_feature.txt"
ATTRI_NON_CONNS_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "attri_non_conns_dev_feature.txt"

PS_ARG2_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "ps_arg2_train_feature.txt"
PS_ARG2_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "ps_arg2_dev_feature.txt"

PS_ARG1_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "ps_arg1_train_feature.txt"
PS_ARG1_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "ps_arg1_dev_feature.txt"

IMPLICIT_ARG1_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "implicit_arg1_train_feature.txt"
IMPLICIT_ARG1_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "implicit_arg1_dev_feature.txt"

IMPLICIT_ARG2_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "implicit_arg2_train_feature.txt"
IMPLICIT_ARG2_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "implicit_arg2_dev_feature.txt"


COMP_CONTRAST_TRAIN_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "comp_contrast_train_feature.txt"
COMP_CONTRAST_DEV_FEATURE_OUTPUT_PATH = FEATURE_OUTPUT_PATH + "comp_contrast_dev_feature.txt"

''' -- dev output --- '''
DEV_OUTPUT_PATH = CWD + "model_trainer/dev_output/"
# connective
CONNECTIVE_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "connective_dev_result.txt"
#arg_positon
ARG_POSITION_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "arg_position_dev_result.txt"
#arg_extractor
ARG_EXTRACTOR_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "arg_extractor_dev_result.txt"
ARG_EXTRACTOR_DEV_EVALUATION_PATH = DEV_OUTPUT_PATH + "arg_extractor_dev_evaluation.txt"
#nt arg_extractor
NT_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "nt_dev_result.txt"
#explicit
EXPLICIT_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "explicit_dev_result.txt"
#non_explicit
NON_EXPLICIT_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "non_explicit_dev_result.txt"
#attri
ATTRI_NON_CONNS_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "attri_non_conns_dev_result.txt"
# ps arg2
PS_ARG2_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "ps_arg2_dev_result.txt"
# ps arg1
PS_ARG1_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "ps_arg1_dev_result.txt"
# comp contrast
COMP_CONTRAST_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "comp_contrast_dev_result.txt"
# implicit arg1
IMPLICIT_ARG1_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "implicit_arg1_dev_result.txt"
# implicit arg2
IMPLICIT_ARG2_DEV_OUTPUT_PATH = DEV_OUTPUT_PATH + "implicit_arg2_dev_result.txt"

MODEL_PATH = CWD + "model/"
#connective classifier model
CONNECTIVE_CLASSIFIER_MODEL = MODEL_PATH + "connective_classifier.model"
# argument position classifer
ARG_POSITION_CLASSIFIER_MODEL = MODEL_PATH + "arg_position_classifier.model"
# argument extractor
ARG_EXTRACTOR_CLASSIFIER_MODEL = MODEL_PATH + "arg_extractor_classifier.model"
# NT
NT_CLASSIFIER_MODEL = MODEL_PATH + "nt_classifier.model"
#explicit
EXPLICIT_CLASSIFIER_MODEL = MODEL_PATH + "explicit_classifier.model"
#non-explicit
NON_EXPLICIT_CLASSIFIER_MODEL = MODEL_PATH + "non_explicit_classifier.model"
# ps arg2
PS_ARG2_CLASSIFIER_MODEL = MODEL_PATH + "ps_arg2_classifier.model"
# ps arg1
PS_ARG1_CLASSIFIER_MODEL = MODEL_PATH + "ps_arg1_classifier.model"
# implicit arg1
IMPLICIT_ARG1_CLASSIFIER_MODEL = MODEL_PATH + "implicit_arg1_classifier.model"
# implicit arg2
IMPLICIT_ARG2_CLASSIFIER_MODEL = MODEL_PATH + "implicit_arg2_classifier.model"



''' connective syntatic category '''
CONNECTIVE_CATEGORY_PATH = DATA_PATH + "connective-category.txt"
adverbial = "adverbial"
Subordinator = "subordinator"
Coordinator = "coordinator"


Sense_To_Label = {
        'Temporal.Asynchronous.Precedence': '1',
		'Temporal.Asynchronous.Succession': '2',
		'Temporal.Synchrony': '3',
		'Contingency.Cause.Reason': '4',
		'Contingency.Cause.Result': '5',
		'Contingency.Condition': '6',
		'Comparison.Contrast': '7',
		'Comparison.Concession': '8',
		'Expansion.Conjunction': '9',
		'Expansion.Instantiation': '10',
		'Expansion.Restatement': '11',
		'Expansion.Alternative': '12',
		'Expansion.Alternative.Chosen alternative': '13',
		'Expansion.Exception': '14',
        'EntRel': '15',
        # 'Comparison': '16',
        # 'Contingency': '17',
        # 'Expansion': '18',
        # 'Temporal': '19',
        # 'Contingency.Cause': '20',
        # 'Temporal.Asynchronous': '21'
}

Label_To_Sense = {
        '1':'Temporal.Asynchronous.Precedence',
		'2':'Temporal.Asynchronous.Succession',
		'3':'Temporal.Synchrony',
		'4':'Contingency.Cause.Reason',
		'5':'Contingency.Cause.Result',
		'6':'Contingency.Condition',
		'7':'Comparison.Contrast',
		'8':'Comparison.Concession',
		'9':'Expansion.Conjunction',
		'10':'Expansion.Instantiation',
		'11':'Expansion.Restatement',
		'12':'Expansion.Alternative',
		'13':'Expansion.Alternative.Chosen alternative',
		'14':'Expansion.Exception',
        '15':'EntRel',
        # '16':'Comparison',
        # '17':'Contingency',
        # '18':'Expansion',
        # '19':'Temporal',
        # '20': 'Contingency.Cause',
        # '21': 'Temporal.Asynchronous'
}

SENSES = [
            'Temporal.Asynchronous.Precedence',
            'Temporal.Asynchronous.Succession',
            'Temporal.Synchrony',
            'Contingency.Cause.Reason',
            'Contingency.Cause.Result',
            'Contingency.Condition',
            'Comparison.Contrast',
            'Comparison.Concession',
            'Expansion.Conjunction',
            'Expansion.Instantiation',
            'Expansion.Restatement',
            'Expansion.Alternative',
            'Expansion.Alternative.Chosen alternative',
            'Expansion.Exception',
            'EntRel',
]


JSON_DEV_OUTPUT_PATH = CWD + "data/test.json"
JSON_GOLD_EXPLICIT_PATH =CWD + "data/gold_explicit.json"
JSON_GOLD_NON_EXPLICIT_PATH =CWD + "data/gold_non_explicit.json"

NEGATE_WORDS_PATH =  CWD + "data/negate_word"
LCSINFOMERGE_PATH = CWD + "data/LCSInfomerge.txt"

INQUIRER_WORD_PATH = CWD + "data/inquirer_word"
POLARITY_WORD_PATH = CWD + "data/polarity_word"


PARSER_OUTPUT = CWD + "parser_output/"
PARSER_FEATURE = PARSER_OUTPUT + "feature/"
PARSER_MODEL_OUTPUT = PARSER_OUTPUT + "model_output/"

''' conn_clf '''
PARSER_CONN_CLF_FEATURE = PARSER_FEATURE + "conn_clf_feature.txt"
PARSER_CONN_CLF_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "conn_clf_model_output.txt"

''' arg position clf '''
PARSER_ARG_POSITION_FEATURE = PARSER_FEATURE + "arg_position_feature.txt"
PARSER_ARG_POSITION_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "arg_position_model_output.txt"

''' constituent clf '''
PARSER_CONSTITUENT_FEATURE = PARSER_FEATURE + "constituent_feature.txt"
PARSER_CONSTITUENT_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "constituent_model_output.txt"

''' explicit clf '''
PARSER_EXPLICIT_CLF_FEATURE = PARSER_FEATURE + "explicit_clf_feature.txt"
PARSER_EXPLICIT_CLF_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "explicit_clf_model_output.txt"

''' explicit ps arg2 extractor '''
PARSER_PS_ARG2_FEATURE = PARSER_FEATURE + "ps_arg2_feature.txt"
PARSER_PS_ARG2_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "ps_arg2_model_output.txt"

''' explicit ps arg1 extractor '''
PARSER_PS_ARG1_FEATURE = PARSER_FEATURE + "ps_arg1_feature.txt"
PARSER_PS_ARG1_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "ps_arg1_model_output.txt"

''' implicit arg1 extractor '''
PARSER_IMPLICIT_ARG1_FEATURE = PARSER_FEATURE + "implicit_arg1_feature.txt"
PARSER_IMPLICIT_ARG1_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "implicit_arg1_model_output.txt"

''' implicit arg2 extractor '''
PARSER_IMPLICIT_ARG2_FEATURE = PARSER_FEATURE + "implicit_arg2_feature.txt"
PARSER_IMPLICIT_ARG2_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "implicit_arg2_model_output.txt"

''' explicit relation json file '''
PARSER_EXPLICIT_REATION_PATH = PARSER_OUTPUT + "pred_explicit_relation.json"
''' non-explicit relation json file '''
PARSER_NON_EXPLICIT_REATION_PATH = PARSER_OUTPUT + "pred_non_explicit_relation.json"
'''  relation json file '''
PARSER_REATION_PATH = PARSER_OUTPUT + "pred_relation.json"

''' non_explicit clf '''
PARSER_NON_EXPLICIT_CLF_FEATURE = PARSER_FEATURE + "non_explicit_clf_feature.txt"
PARSER_NON_EXPLICIT_CLF_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "non_explicit_clf_model_output.txt"

''' attribution clf '''
PARSER_ATTRI_NON_CONNS_CLF_FEATURE = PARSER_FEATURE + "attri_non_conns_clf_feature.txt"
PARSER_ATTRI_NON_CONNS_CLF_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "attri_non_conns_clf_model_output.txt"

''' Explicit PS attribution clf '''
PARSER_PS_EXP_ATTRI_CLF_FEATURE = PARSER_FEATURE + "ps_exp_attri_clf_feature.txt"
PARSER_PS_EXP_ATTRI_CLF_MODEL_OUTPUT = PARSER_MODEL_OUTPUT + "aps_exp_attri_clf_model_output.txt"


ARG_POSITION_TO_LABEL = {
    "SS": '0',
    "PS": '1'
}
LABEL_TO_ARG_POSITION = {
    "0": 'SS',
    "1": 'PS'
}

# word2Vec
SKIPGRAM_WORD_EMBEDDING_FILE = CWD + "data/GoogleNews-vectors-negative300.bin"
#freely_omissible_connectives
FREELY_OMISSIBLE_CONNECTIVES_PATH = CWD + "data/freely_omissible_connectives.txt"

FEATURE_SELECTION_PATH = CWD + "feature_selection/"

FEATURE_SELECTION_PRODUCTION_RULES = FEATURE_SELECTION_PATH + "production_rules.txt"
FEATURE_SELECTION_PRODUCTION_RULES_INFOGAIN = FEATURE_SELECTION_PATH + "production_rules_infoGain.txt"
FEATURE_SELECTION_DICT_TOP_N_PRODUCTION_RULES = FEATURE_SELECTION_PATH + "top_nproduction_rules.txt"
# brown cluster
FEATURE_SELECTION_BROWN_CLUSTER = FEATURE_SELECTION_PATH + "brown_cluster.txt"
FEATURE_SELECTION_BROWN_CLUSTER_INFOGAIN = FEATURE_SELECTION_PATH + "brown_cluster_infoGain.txt"
FEATURE_SELECTION_DICT_TOP_N_BROWN_CLUSTER = FEATURE_SELECTION_PATH + "top_n_brown_cluster.txt"


MPQA_SUBJECTIVITY_LEXICON_PATH = CWD + "data/MPQA_Subjectivity_Lexicon.txt"
VERB_NET_PATH = CWD + "data/new_vn"

PDTB_IMPILICIT_CONNECTIVE = DICT_PATH + "pdtb_implicit_connective"
LM = CWD + "data/ny_ord5.lm"
INPUT_LM = CWD + "data/input_lm"
OUTPUT_LM = CWD + "data/output_lm.ppl"

XUYU_CONNS = CWD + "dict/xuyu_conns.txt"

FREELY_OMISSIBLE_CONN_LIST_PATH = CWD + "data/freely_omissible_conn_list.txt"
WORD2VEC_CONNS_PATH = CWD + "dict/word2vec_conns.txt"
