#coding:utf-8
from util import singleton
import util, config

@singleton
class Ps_arg1_dict():
    def __init__(self):
        self.dict_lowercase_verbs = \
            util.load_dict_from_file(config.PS_ARG1_DICT_LOWERCASE_VERBS)

        self.dict_lemma_verbs = \
            util.load_dict_from_file(config.PS_ARG1_DICT_LEMMA_VERBS)

        self.dict_curr_first = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CURR_FIRST)

        self.dict_curr_last = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CURR_LAST)

        self.dict_prev_last = \
            util.load_dict_from_file(config.PS_ARG1_DICT_PREV_LAST)

        self.dict_next_first = \
            util.load_dict_from_file(config.PS_ARG1_DICT_NEXT_FIRST)

        self.dict_prev_last_curr_first = \
            util.load_dict_from_file(config.PS_ARG1_DICT_PREV_LAST_CURR_FIRST)

        self.dict_curr_last_next_first = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CURR_LAST_NEXT_FIRST)

        self.dict_curr_production_rule = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CURR_PRODUCTION_RULE)

        self.dict_con_str = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_STR)

        self.dict_con_lstr = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_LSTR)


        self.dict_conn_to_root_path = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_TO_ROOT_PATH)

        self.dict_conn_to_root_compressed_path = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_TO_ROOT_COMPRESSED_PATH)

        self.dict_conn_curr_position = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_CURR_POSITION)

        self.dict_curr_first_prev_last_parse_path = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CURR_FIRST_PREV_LAST_PARSE_PATH)

        self.dict_conn_curr_first = \
            util.load_dict_from_file(config.PS_ARG1_DICT_CONN_CURR_FIRST)

