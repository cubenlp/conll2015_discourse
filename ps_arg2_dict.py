#coding:utf-8
from util import singleton
import util, config

@singleton
class Ps_arg2_dict():
    def __init__(self):
        self.dict_lowercase_verbs = \
            util.load_dict_from_file(config.PS_ARG2_DICT_LOWERCASE_VERBS)

        self.dict_lemma_verbs = \
            util.load_dict_from_file(config.PS_ARG2_DICT_LEMMA_VERBS)

        self.dict_curr_first = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_FIRST)

        self.dict_curr_last = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_LAST)

        self.dict_prev_last = \
            util.load_dict_from_file(config.PS_ARG2_DICT_PREV_LAST)

        self.dict_next_first = \
            util.load_dict_from_file(config.PS_ARG2_DICT_NEXT_FIRST)

        self.dict_prev_last_curr_first = \
            util.load_dict_from_file(config.PS_ARG2_DICT_PREV_LAST_CURR_FIRST)

        self.dict_curr_last_next_first = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_LAST_NEXT_FIRST)

        self.dict_curr_production_rule = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_PRODUCTION_RULE)

        self.dict_con_str = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_STR)
        self.dict_con_lstr = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_LSTR)

        self.dict_conn_position_distance = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_POSITION_DISTANCE)

        self.dict_prev_curr_CP_production_rule = \
            util.load_dict_from_file(config.PS_ARG2_DICT_PREV_CURR_CP_PRODUCTION_RULE)

        self.dict_conn_to_root_path = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_TO_ROOT_PATH)

        self.dict_conn_to_root_compressed_path = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_TO_ROOT_COMPRESSED_PATH)

        self.dict_conn_position = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_POSITION)

        self.dict_conn_is_adjacent_to_conn = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_IS_ADJACENT_TO_CONN)

        self.dict_curr_first_curr_first_lemma_verb = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_FIRST_CURR_FIRST_LEMMA_VERB)

        self.dict_curr_first_lowercased_verb = \
            util.load_dict_from_file(config.PS_ARG2_DICT_FIRST_LOWERCASE_VERB)

        self.dict_curr_first_lemma_verb = \
            util.load_dict_from_file(config.PS_ARG2_DICT_FIRST_LEMMA_VERB)

        self.dict_curr_first_prev_last_parse_path = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CURR_FIRST_PREV_LAST_PARSE_PATH)

        self.dict_CParent_to_root_path_node_names = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)

        self.dict_CPOS = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CPOS)

        self.dict_conn_connCtx = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_CONNCTX)

        self.dict_conn_parent_category_Ctx = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_PARENT_CATEGORY_CTX)

        self.dict_conn_curr_first = \
            util.load_dict_from_file(config.PS_ARG2_DICT_CONN_CURR_FIRST)
