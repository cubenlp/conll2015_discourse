#coding:utf-8
from util import singleton
import util, config

@singleton
class Explicit_dict():
    def __init__(self):
        self.dict_CString = self.get_dict_CString()
        self.dict_CPOS = self.get_dict_CPOS()
        self.dict_C_Prev = self.get_dict_C_Prev()

        self.dict_CLString = self.get_dict_CLString()

        self.self_category_dict = self.get_self_category_dict()
        self.parent_category_dict = self.get_parent_category_dict()
        self.left_sibling_category_dict = self.get_left_sibling_category_dict()
        self.right_sibling_category_dict = self.get_right_sibling_category_dict()

        self.conn_self_category_dict = self.get_conn_self_category_dict()
        self.conn_parent_category_dict = self.get_conn_parent_category_dict()
        self.conn_left_sibling_category_dict = self.get_conn_left_sibling_category_dict()
        self.conn_right_sibling_category_dict = self.get_conn_right_sibling_category_dict()

        self.self_parent_dict = util.load_dict_from_file(config.EXPLICIT_DICT_SELF_PARENT_CATEGORY_PATH)
        self.self_right_dict = util.load_dict_from_file(config.EXPLICIT_DICT_SELF_RIGHT_CATEGORY_PATH)
        self.self_left_dict = util.load_dict_from_file(config.EXPLICIT_DICT_SELF_LEFT_CATEGORY_PATH)
        self.parent_left_dict = util.load_dict_from_file(config.EXPLICIT_DICT_PARENT_LEFT_CATEGORY_PATH)
        self.parent_right_dict = util.load_dict_from_file(config.EXPLICIT_DICT_PARENT_RIGHT_CATEGORY_PATH)
        self.left_right_dict = util.load_dict_from_file(config.EXPLICIT_DICT_LEFT_RIGHT_CATEGORY_PATH)


        ''' mine '''
        self.dict_conn_to_root_path = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_TO_ROOT_PATH)
        self.dict_conn_next = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_NEXT)
        self.dict_conn_connCtx = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_CONNCTX)
        self.dict_conn_rightSiblingCtx = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_RIGHTSIBLINGCTX)
        self.dict_conn_parent_category_ctx = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_CTX)
        self.dict_conn_leftSibling_ctx = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_LEFTSIBLING_CTX)
        self.dict_CParent_to_root_path_node_names = util.load_dict_from_file(config.EXPLICIT_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)
        self.dict_conn_parent_category_not_linked_ctx = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_NOT_LINKED_CTX)
        self.dict_conn_prev_conn = util.load_dict_from_file(config.EXPLICIT_DICT_CONN_PREV_CONN)
        self.dict_prev_conn = util.load_dict_from_file(config.EXPLICIT_DICT_PREV_CONN)
        self.dict_as_prev_conn = util.load_dict_from_file(config.EXPLICIT_DICT_AS_PREV_CONN)
        self.dict_as_prev_connPOS = util.load_dict_from_file(config.EXPLICIT_DICT_AS_PREV_CONNPOS)
        self.dict_when_prev_conn = util.load_dict_from_file(config.EXPLICIT_DICT_WHEN_PREV_CONN)
        self.dict_when_prev_connPOS = util.load_dict_from_file(config.EXPLICIT_DICT_WHEN_PREV_CONNPOS)

        self.dict_as_before_after_tense = util.load_dict_from_file(config.EXPLICIT_DICT_AS_BEFORE_AFTER_TENSE)
        self.dict_when_before_after_tense = util.load_dict_from_file(config.EXPLICIT_DICT_WHEN_BEFORE_AFTER_TENSE)
        self.dict_when_after_lemma_verbs = util.load_dict_from_file(config.EXPLICIT_DICT_WHEN_AFTER_LEMMA_VERBS)



    def get_dict_CString(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CSTRING)

    def get_dict_CPOS(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CPOS)

    def get_dict_C_Prev(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_C_PREV)

    def get_dict_CLString(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CLSTRING)

    def get_self_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_SELF_CATEGORY_PATH)

    def get_parent_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_PARENT_CATEGORY_PATH)

    def get_left_sibling_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_LEFT_SIBLING_CATEGORY_PATH)

    def get_right_sibling_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_RIGHT_SIBLING_CATEGORY_PATH)

    def get_conn_self_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CONN_SELF_CATEGORY_PATH)

    def get_conn_parent_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CONN_PARENT_CATEGORY_PATH)

    def get_conn_left_sibling_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH)

    def get_conn_right_sibling_category_dict(self):
        return util.load_dict_from_file(config.EXPLICIT_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH)









