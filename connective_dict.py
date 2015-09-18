#coding:utf-8
from util import singleton
import util, config

@singleton
class Connectives_dict():
    def __init__(self):
        self.sorted_conns_list = self.get_sorted_conns_list()
        self.cpos_dict = self.get_CPOS_dict()
        self.prev_C_dict = self.get_prev_C_dict()
        self.prevPOS_dict = self.get_prevPOS_dict()
        self.prevPOS_CPOS_dict = self.get_prevPOS_CPOS_dict()
        self.C_next_dict = self.get_C_next_dict()
        self.nextPOS_dict = self.get_nextPOS_dict()
        self.CPOS_nextPOS_dict = self.get_CPOS_nextPOS()
        self.CParent_to_root_path_dict = self.get_CParent_to_root_path_dict()
        self.compressed_CParent_to_root_path_dict = self.get_compressed_CParent_to_root_path_dict()

        self.self_category_dict = self.get_self_category_dict()
        self.parent_category_dict = self.get_parent_category_dict()
        self.left_sibling_category_dict = self.get_left_sibling_category_dict()
        self.right_sibling_category_dict = self.get_right_sibling_category_dict()

        self.conn_self_category_dict = self.get_conn_self_category_dict()
        self.conn_parent_category_dict = self.get_conn_parent_category_dict()
        self.conn_left_sibling_category_dict = self.get_conn_left_sibling_category_dict()
        self.conn_right_sibling_category_dict = self.get_conn_right_sibling_category_dict()

        self.self_parent_dict = self.get_self_parent_dict()
        self.self_right_dict = self.get_self_right_dict()
        self.self_left_dict = self.get_self_left_dict()
        self.parent_left_dict = self.get_parent_left_dict()
        self.parent_right_dict = self.get_parent_right_dict()
        self.left_right_dict = self.get_left_right_dict()

        self.conn_category = self.get_conn_category_dict()

        ''' mine '''
        self.dict_conn_lower_case = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_LOWER_CASE)
        self.dict_conn = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN)
        self.dict_prevPOS_C = util.load_dict_from_file(config.CONNECTIVE_DICT_PREVPOS_C)
        self.dict_self_category_to_root_path = util.load_dict_from_file(config.CONNECTIVE_DICT_SELF_CATEGORY_TO_ROOT_PATH)
        self.dict_CParent_to_root_path_node_names = util.load_dict_from_file(config.CONNECTIVE_DICT_CPARENT_TO_ROOT_PATH_NODE_NAMES)
        self.dict_conn_connCtx = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_CONNCTX)
        self.dict_conn_rightSiblingCtx = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_RIGHTSIBLINGCTX)
        self.dict_conn_leftSiblingCtx = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_LEFTSIBLINGCTX)
        self.dict_conn_left_right_SiblingCtx = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_LEFT_RIGHT_SIBLINGCTX)
        self.dict_conn_parent_category_Ctx = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_PARENT_CATEGORY_CTX)
        self.dict_rightSibling_production_rules = util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_RIGHTSIBLING_PRODUCTION_RULES)




        # print "connective dict is loaded ...."

    def get_sorted_conns_list(self):
        # print "loading sorted_conns_list ..."
        return util.load_list_from_file(config.SORTED_ExpConn_PATH)

    def get_CPOS_dict(self):
        # print "loading c pos ..."
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CPOS_PATH)

    def get_prev_C_dict(self):
        # print "loading c pre.."
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PREV_C_PATH)

    def get_prevPOS_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PREVPOS_PATH)

    def get_prevPOS_CPOS_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PREVPOS_CPOS_PATH)

    def get_C_next_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_C_NEXT_PATH)

    def get_nextPOS_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_NEXTPOS_PATH)

    def get_CPOS_nextPOS(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CPOS_NEXTPOS_PATH)

    def get_CParent_to_root_path_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CPARENT_TO_ROOT_PATH)

    def get_compressed_CParent_to_root_path_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_COMPRESSED_CPARENT_TO_ROOT_PATH)

    def get_self_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_SELF_CATEGORY_PATH)

    def get_parent_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PARENT_CATEGORY_PATH)

    def get_left_sibling_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_LEFT_SIBLING_CATEGORY_PATH)

    def get_right_sibling_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_RIGHT_SIBLING_CATEGORY_PATH)

    def get_conn_self_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_SELF_CATEGORY_PATH)

    def get_conn_parent_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_PARENT_CATEGORY_PATH)

    def get_conn_left_sibling_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_LEFT_SIBLING_CATEGORY_PATH)

    def get_conn_right_sibling_category_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_CONN_RIGHT_SIBLING_CATEGORY_PATH)

    def get_self_parent_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_SELF_PARENT_CATEGORY_PATH)

    def get_self_right_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_SELF_RIGHT_CATEGORY_PATH)

    def get_self_left_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_SELF_LEFT_CATEGORY_PATH)

    def get_parent_left_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PARENT_LEFT_CATEGORY_PATH)

    def get_parent_right_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_PARENT_RIGHT_CATEGORY_PATH)

    def get_left_right_dict(self):
        return util.load_dict_from_file(config.CONNECTIVE_DICT_LEFT_RIGHT_CATEGORY_PATH)

    def get_conn_category_dict(self):
        dict = {}
        file = open(config.CONNECTIVE_CATEGORY_PATH)
        lines = [line.strip() for line in file.readlines()]
        for line in lines:
            list = line.split("#")
            conn = list[0].strip()
            category = list[1].strip()
            dict[conn] = category
        return dict

