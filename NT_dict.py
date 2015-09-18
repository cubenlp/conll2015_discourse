#coding:utf-8
from util import singleton
import util, config

@singleton
class NT_dict():
    def __init__(self):
        self.dict_CON_Str = self.get_dict_CON_Str()
        self.dict_CON_LStr = self.get_dict_CON_LStr()
        self.dict_NT_Ctx = self.get_dict_NT_Ctx()
        self.dict_CON_NT_Path = self.get_dict_CON_NT_Path()
        self.dict_CON_NT_Path_iLsib = self.get_dict_CON_NT_Path_iLsib()

        self.dict_NT_prev_curr_Path = util.load_dict_from_file(config.NT_DICT_PREV_CURR_PATH)
        self.dict_CON_POS = util.load_dict_from_file(config.NT_DICT_CON_POS)
        self.dict_C_Prev = util.load_dict_from_file(config.NT_DICT_C_PREV)
        self.dict_NT_Name = util.load_dict_from_file(config.NT_DICT_NT_NAME)

        self.dict_NT_prev_curr_production_rule = util.load_dict_from_file(config.NT_DICT_NT_PREV_CURR_PRODUCTION_RULE)

        self.dict_nt_ntParent_ctx = util.load_dict_from_file(config.NT_DICT_NT_NTPARENT_CTX)

        self.dict_CParent_to_root_path = util.load_dict_from_file(config.NT_DICT_CPARENT_TO_ROOT_PATH)
        self.dict_CParent_to_root_path_node_names = util.load_dict_from_file(config.NT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)
        self.dict_conn_connCtx = util.load_dict_from_file(config.NT_DICT_CONN_CONNCTX)
        self.dict_conn_parent_categoryCtx = util.load_dict_from_file(config.NT_DICT_CONN_PARENT_CATEGORYCTX)
        self.dict_conn_rightSiblingCtx = util.load_dict_from_file(config.NT_DICT_CONN_RIGHTSIBLINGCTX)
        self.dict_self_category = util.load_dict_from_file(config.NT_DICT_SELF_CATEGORY)
        self.dict_parent_category = util.load_dict_from_file(config.NT_DICT_PARENT_CATEGORY)
        self.dict_left_sibling_category = util.load_dict_from_file(config.NT_DICT_LEFT_SIBLING_CATEGORY)
        self.dict_right_sibling_category = util.load_dict_from_file(config.NT_DICT_RIGHT_SIBLING_CATEGORY)

        self.dict_NT_Linked_ctx = util.load_dict_from_file(config.NT_DICT_NT_LINKED_CTX)
        self.dict_NT_to_root_path = util.load_dict_from_file(config.NT_DICT_NT_TO_ROOT_PATH)
        self.dict_NT_parent_linked_ctx = util.load_dict_from_file(config.NT_DICT_NT_PARENT_LINKED_CTX)




        # print "NT_dict is loaded..."






    def get_dict_CON_Str(self):
        return util.load_dict_from_file(config.NT_DICT_CON_Str)

    def get_dict_CON_LStr(self):
        return util.load_dict_from_file(config.NT_DICT_CON_LStr)

    def get_dict_NT_Ctx(self):
        return util.load_dict_from_file(config.NT_DICT_NT_Ctx)

    def get_dict_CON_NT_Path(self):
        return util.load_dict_from_file(config.NT_DICT_CON_NT_Path)

    def get_dict_CON_NT_Path_iLsib(self):
        return util.load_dict_from_file(config.NT_DICT_CON_NT_Path_iLsib)






