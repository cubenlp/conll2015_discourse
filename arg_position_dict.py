#coding:utf-8
from util import singleton
import util, config

@singleton
class Arg_position_dict():
    def __init__(self):
        self.dict_CString = self.get_dict_CString()
        self.dict_CPOS = self.get_dict_CPOS()
        self.dict_prev1 = self.get_dict_prev1()
        self.dict_prev1POS = self.get_dict_prev1POS()
        self.dict_prev1_C = self.get_dict_prev1_C()
        self.dict_prev1POS_CPOS = self.get_dict_prev1POS_CPOS()
        self.dict_prev2 = self.get_dict_prev2()
        self.dict_prev2POS = self.get_dict_prev2POS()
        self.dict_prev2_C = self.get_dict_prev2_C()
        self.dict_prev2POS_CPOS = self.get_dict_prev2POS_CPOS()

        self.dict_next1 = self.get_dict_next1()
        self.dict_next1POS = self.get_dict_next1POS()
        self.dict_next1_C = self.get_dict_next1_C()
        self.dict_next1POS_CPOS = self.get_dict_next1POS_CPOS()
        self.dict_next2 = self.get_dict_next2()
        self.dict_next2POS = self.get_dict_next2POS()
        self.dict_next2_C = self.get_dict_next2_C()
        self.dict_next2POS_CPOS = self.get_dict_next2POS_CPOS()

        self.dict_conn_to_root_path = util.load_dict_from_file(config.ARG_POSITION_DICT_CONN_TO_ROOT_PATH)

        # print "Arg_position_dict is loaded..."

    def get_dict_CString(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_CSTRING)

    def get_dict_CPOS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_CPOS)

    def get_dict_prev1(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV1)

    def get_dict_prev1POS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV1POS)

    def get_dict_prev1_C(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV1_C)

    def get_dict_prev1POS_CPOS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV1POS_CPOS)

    def get_dict_prev2(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV2)

    def get_dict_prev2POS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV2POS)

    def get_dict_prev2_C(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV2_C)

    def get_dict_prev2POS_CPOS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_PREV2POS_CPOS)

    def get_dict_next1(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT1)

    def get_dict_next1POS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT1POS)

    def get_dict_next1_C(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT1_C)

    def get_dict_next1POS_CPOS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT1POS_CPOS)

    def get_dict_next2(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT2)

    def get_dict_next2POS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT2POS)

    def get_dict_next2_C(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT2_C)

    def get_dict_next2POS_CPOS(self):
        return util.load_dict_from_file(config.ARG_POSITION_DICT_NEXT2POS_CPOS)



