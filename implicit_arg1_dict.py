#coding:utf-8
from util import singleton
import util, config

@singleton
class Implicit_arg1_dict():
    def __init__(self):
        self.dict_lowercase_verbs = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_LOWERCASE_VERBS)

        self.dict_lemma_verbs = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_LEMMA_VERBS)

        self.dict_curr_first = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_FIRST)

        self.dict_curr_last = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_LAST)

        self.dict_prev_last = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_PREV_LAST)

        self.dict_next_first = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_NEXT_FIRST)

        self.dict_prev_last_curr_first = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_PREV_LAST_CURR_FIRST)

        self.dict_curr_last_next_first = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_LAST_NEXT_FIRST)

        self.dict_curr_production_rule = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_PRODUCTION_RULE)

        self.dict_prev_curr_production_rule = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_PREV_CURR_PRODUCTION_RULE)

        self.dict_prev_curr_CP_production_rule = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_PREV_CURR_CP_PRODUCTION_RULE)

        self.dict_curr_next_CP_production_rule = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_NEXT_CP_PRODUCTION_RULE)

        self.dict_prev2_pos_lemma_verb = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_2PREV_POS_LEMMA_VERB)

        self.dict_curr_first_to_prev_last_path = \
            util.load_dict_from_file(config.IMPLICIT_ARG1_DICT_CURR_FIRST_TO_PREV_LAST_PATH)







