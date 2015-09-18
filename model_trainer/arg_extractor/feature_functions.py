#coding:utf-8
from feature import Feature
import util
from arg_extractor_dict import Arg_extractor_dict
from syntax_tree import Syntax_tree
import arg_extractor_dict_util  as dict_util

def all_features(syntax_tree, connective, node, parse_dict):
    ''' feat dict '''

    feat_dict_C_String = {}
    feat_dict_C_Category = {}
    feat_dict_C_left_sibling_number = {}
    feat_dict_C_right_sibling_number = {}
    feat_dict_CParent_to_Node_path = {}
    feat_dict_CParent_to_Node_path_left_sibling_number = {}
    feat_dict_relative_position = {}
    feat_dict_CParent_to_Node_path_length = {}


    ''' load dict '''
    dict_C_String = Arg_extractor_dict().dict_C_String
    dict_C_Category = Arg_extractor_dict().dict_C_Category
    dict_C_left_sibling_number = Arg_extractor_dict().dict_C_left_sibling_number
    dict_C_right_sibling_number = Arg_extractor_dict().dict_C_right_sibling_number
    dict_CParent_to_Node_path = Arg_extractor_dict().dict_CParent_to_Node_path
    dict_CParent_to_Node_path_left_sibling_number = Arg_extractor_dict().dict_CParent_to_Node_path_left_sibling_number
    dict_relative_position = Arg_extractor_dict().dict_relative_position
    dict_CParent_to_Node_path_length = Arg_extractor_dict().dict_CParent_to_Node_path_length

    ''' feature '''
    #获取该句话的语法树
    conn_indices = connective.token_indices
    DocID = connective.DocID
    sent_index = connective.sent_index


    C_String = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    C_Category = connective.category
    C_left_sibling_number = dict_util.get_C_left_sibling_number(syntax_tree, conn_indices)
    C_right_sibling_number = dict_util.get_C_right_sibling_number(syntax_tree, conn_indices)

    CParent_to_Node_path = dict_util.get_CParent_to_Node_path(syntax_tree, conn_indices, node)
    if C_left_sibling_number > 1:
        CParent_to_Node_path_left_sibling_number = CParent_to_Node_path + "&" + "yes"
    else:
        CParent_to_Node_path_left_sibling_number = CParent_to_Node_path + "&" + "no"
    relative_position = dict_util.get_relative_position_Node_to_C(syntax_tree, conn_indices, node)

    CParent_to_Node_path_length = dict_util.get_CParent_to_Node_path_length(syntax_tree, conn_indices, node)


    features = []
    features.append(get_feature(feat_dict_C_String, dict_C_String,C_String ))
    features.append(get_feature(feat_dict_C_Category, dict_C_Category, C_Category))

    # features.append(Feature("", 1, {1: C_left_sibling_number}))
    # features.append(Feature("", 1, {1: C_right_sibling_number}))

    features.append(get_feature(feat_dict_C_left_sibling_number, dict_C_left_sibling_number, C_left_sibling_number))
    features.append(get_feature(feat_dict_C_right_sibling_number, dict_C_right_sibling_number, C_right_sibling_number))

    features.append(get_feature(feat_dict_CParent_to_Node_path, dict_CParent_to_Node_path, CParent_to_Node_path))
    features.append(get_feature(feat_dict_CParent_to_Node_path_left_sibling_number, dict_CParent_to_Node_path_left_sibling_number, CParent_to_Node_path_left_sibling_number))
    features.append(get_feature(feat_dict_relative_position, dict_relative_position, relative_position))
    # features.append(get_feature(feat_dict_CParent_to_Node_path_length, dict_CParent_to_Node_path_length, CParent_to_Node_path_length))


    return util.mergeFeatures(features)




def get_feature(feat_dict, dict, feat):
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)