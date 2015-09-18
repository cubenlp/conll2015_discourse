#coding:utf-8
from util import singleton
import util, config

@singleton
class Arg_extractor_dict():
    def __init__(self):


        self.dict_C_String = self.get_dict_C_String()
        self.dict_C_Category = self.get_dict_C_Category()
        self.dict_C_left_sibling_number = self.get_dict_C_left_sibling_number()
        self.dict_C_right_sibling_number = self.get_dict_C_right_sibling_number()
        self.dict_CParent_to_Node_path = self.get_dict_CParent_to_Node_path()
        self.dict_CParent_to_Node_path_left_sibling_number = self.get_dict_CParent_to_Node_path_left_sibling_number()
        self.dict_relative_position = self.get_dict_relative_position()
        self.dict_CParent_to_Node_path_length = self.get_dict_CParent_to_Node_path_length()


        print "Arg_extractor_dict is loaded..."



    def get_dict_C_String(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_STRING)

    def get_dict_C_Category(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_CATEGORY)

    def get_dict_C_left_sibling_number(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_LEFT_SIBLING_NUMBER)

    def get_dict_C_right_sibling_number(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_RIGHT_SIBLING_NUMBER)

    def get_dict_CParent_to_Node_path(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH)

    def get_dict_CParent_to_Node_path_left_sibling_number(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH_LEFT_SIBLING_NUMBER)

    def get_dict_relative_position(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_RELATIVE_POSITION)

    def get_dict_CParent_to_Node_path_length(self):
        return util.load_dict_from_file(config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH_LENGTH)





