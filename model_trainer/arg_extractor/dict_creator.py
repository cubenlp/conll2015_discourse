#coding:utf-8
import util
import config
import arg_extractor_dict_util as dict_util
from pdtb_parse import PDTB_PARSE
from connective import Connective
from syntax_tree import Syntax_tree

class Dict_creator:
    def __init__(self, pdtb_parse):
        self.pdtb_parse = pdtb_parse
        self.parse_dict = pdtb_parse.parse_dict

        # dict[(DocID, sent_index)] = [[1], [4,5]]
        self.subordinating_conns_SS = pdtb_parse.pdtb.subordinating_conns_SS
        self.coordinating_conns_SS = pdtb_parse.pdtb.coordinating_conns_SS
        self.adverbial_conns_SS = pdtb_parse.pdtb.adverbial_conns_SS

        self.conns_SS = self.subordinating_conns_SS \
                        + self.coordinating_conns_SS \
                        + self.adverbial_conns_SS

    def create_all_dict(self, threshold = 1):

        print "生成所有 argument extractor 所需字典..."

        dict_C_String = {}
        dict_C_Category = {}
        dict_C_left_sibling_number = {}
        dict_C_right_sibling_number = {}
        dict_CParent_to_Node_path = {}
        dict_CParent_to_Node_path_left_sibling_number = {}
        dict_relative_position = {}
        dict_CParent_to_Node_path_length = {}


        for connective in self.conns_SS:
            #获取该句话的语法树
            DocID = connective.DocID
            sent_index = connective.sent_index
            conn_indices = connective.token_indices
            Arg1_token_indices = connective.Arg1_token_indices
            Arg2_token_indices = connective.Arg2_token_indices

            parse_tree = self.parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
            syntax_tree = Syntax_tree(parse_tree)

            if syntax_tree.tree != None:

                C_String = dict_util.get_C_String(self.parse_dict, DocID, sent_index, conn_indices)
                C_Category = connective.category
                C_left_sibling_number = dict_util.get_C_left_sibling_number(syntax_tree, conn_indices)
                C_right_sibling_number = dict_util.get_C_right_sibling_number(syntax_tree, conn_indices)


                for node in syntax_tree.get_arg1_arg2_None_nodes_list(Arg1_token_indices, Arg2_token_indices):
                    #抽取相应特征
                    CParent_to_Node_path = dict_util.get_CParent_to_Node_path(syntax_tree, conn_indices, node)
                    if C_left_sibling_number > 1:
                        CParent_to_Node_path_left_sibling_number = CParent_to_Node_path + "&" + "yes"
                    else:
                        CParent_to_Node_path_left_sibling_number = CParent_to_Node_path + "&" + "no"
                    relative_position = dict_util.get_relative_position_Node_to_C(syntax_tree, conn_indices, node)

                    CParent_to_Node_path_length = dict_util.get_CParent_to_Node_path_length(syntax_tree, conn_indices, node)

                    util.set_dict_key_value(dict_C_String, C_String)
                    util.set_dict_key_value(dict_C_Category, C_Category)
                    util.set_dict_key_value(dict_C_left_sibling_number, C_left_sibling_number)
                    util.set_dict_key_value(dict_C_right_sibling_number, C_right_sibling_number)
                    util.set_dict_key_value(dict_CParent_to_Node_path, CParent_to_Node_path)
                    util.set_dict_key_value(dict_CParent_to_Node_path_left_sibling_number, CParent_to_Node_path_left_sibling_number)
                    util.set_dict_key_value(dict_relative_position, relative_position)
                    util.set_dict_key_value(dict_CParent_to_Node_path_length, CParent_to_Node_path_length)


         #删除频率小于threshold的键
        util.removeItemsInDict(dict_C_String, threshold)
        util.removeItemsInDict(dict_C_Category, threshold)
        util.removeItemsInDict(dict_C_left_sibling_number, threshold)
        util.removeItemsInDict(dict_C_right_sibling_number, threshold)
        util.removeItemsInDict(dict_CParent_to_Node_path, threshold)
        util.removeItemsInDict(dict_CParent_to_Node_path_left_sibling_number, threshold)
        util.removeItemsInDict(dict_relative_position, threshold)
        util.removeItemsInDict(dict_CParent_to_Node_path_length, threshold)

        #字典keys写入文件

        util.write_dict_keys_to_file(dict_C_String, config.ARG_EXTRACTOR_DICT_C_STRING)
        util.write_dict_keys_to_file(dict_C_Category ,config.ARG_EXTRACTOR_DICT_C_CATEGORY)
        util.write_dict_keys_to_file(dict_C_left_sibling_number, config.ARG_EXTRACTOR_DICT_C_LEFT_SIBLING_NUMBER)
        util.write_dict_keys_to_file(dict_C_right_sibling_number, config.ARG_EXTRACTOR_DICT_C_RIGHT_SIBLING_NUMBER)
        util.write_dict_keys_to_file(dict_CParent_to_Node_path, config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH)
        util.write_dict_keys_to_file(dict_CParent_to_Node_path_left_sibling_number, config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH_LEFT_SIBLING_NUMBER)
        util.write_dict_keys_to_file(dict_relative_position, config.ARG_EXTRACTOR_DICT_C_RELATIVE_POSITION)
        util.write_dict_keys_to_file(dict_CParent_to_Node_path_length, config.ARG_EXTRACTOR_DICT_C_CPARENT_TO_NODE_PATH_LENGTH)



if __name__ == "__main__":
    # create_sorted_exp_conns()
    pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    Dict_creator(pdtb_parse).create_all_dict()

