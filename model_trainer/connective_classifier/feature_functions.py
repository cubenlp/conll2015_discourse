#coding:utf-8

from feature import Feature
from connective_dict import Connectives_dict
from syntax_tree import Syntax_tree
import util
import conn_dict_util as dict_util


def all_features(parse_dict, DocID, sent_index, conn_indices):
    # feat dict
    '''Z.Lin'''
    feat_dict_CPOS_dict = {}
    feat_dict_prev_C_dict = {}
    feat_dict_prevPOS_dict = {}
    feat_dict_prevPOS_CPOS_dict = {}
    feat_dict_C_next_dict = {}
    feat_dict_nextPOS_dict = {}
    feat_dict_CPOS_nextPOS_dict = {}
    feat_dict_CParent_to_root_path_dict = {}
    feat_dict_compressed_CParent_to_root_path_dict = {}

    '''Pitler'''
    feat_dict_self_category_dict = {}
    feat_dict_parent_category_dict = {}
    feat_dict_left_sibling_category_dict = {}
    feat_dict_right_sibling_category_dict = {}
    ''' conn_syn '''
    feat_dict_conn_self_category_dict = {}
    feat_dict_conn_parent_category_dict = {}
    feat_dict_conn_left_sibling_category_dict = {}
    feat_dict_conn_right_sibling_category_dict = {}
    ''' syn_syn '''
    feat_dict_self_parent = {}
    feat_dict_self_right = {}
    feat_dict_self_left = {}
    feat_dict_parent_left = {}
    feat_dict_parent_right = {}
    feat_dict_left_right = {}

    #dict
    '''Z.Lin'''
    CPOS_dict = Connectives_dict().cpos_dict
    prev_C_dict = Connectives_dict().prev_C_dict
    prevPOS_dict = Connectives_dict().prevPOS_dict
    prevPOS_CPOS_dict = Connectives_dict().prevPOS_CPOS_dict
    C_next_dict = Connectives_dict().C_next_dict
    nextPOS_dict = Connectives_dict().nextPOS_dict
    CPOS_nextPOS_dict = Connectives_dict().CPOS_nextPOS_dict
    CParent_to_root_path_dict = Connectives_dict().CParent_to_root_path_dict
    compressed_CParent_to_root_path_dict = Connectives_dict().compressed_CParent_to_root_path_dict

    '''Pitler'''
    self_category_dict = Connectives_dict().self_category_dict
    parent_category_dict = Connectives_dict().parent_category_dict
    left_sibling_category_dict = Connectives_dict().left_sibling_category_dict
    right_sibling_category_dict = Connectives_dict().right_sibling_category_dict
    ''' conn_syn '''
    conn_self_category_dict = Connectives_dict().conn_self_category_dict
    conn_parent_category_dict = Connectives_dict().conn_parent_category_dict
    conn_left_sibling_category_dict = Connectives_dict().conn_left_sibling_category_dict
    conn_right_sibling_category_dict = Connectives_dict().conn_right_sibling_category_dict
    ''' syn_syn '''
    self_parent_dict = Connectives_dict().self_parent_dict
    self_right_dict = Connectives_dict().self_right_dict
    self_left_dict = Connectives_dict().self_left_dict
    parent_left_dict = Connectives_dict().parent_left_dict
    parent_right_dict = Connectives_dict().parent_right_dict
    left_right_dict = Connectives_dict().left_right_dict

    ''' mine '''
    dict_conn_lower_case = Connectives_dict().dict_conn_lower_case
    dict_conn = Connectives_dict().dict_conn
    # dict_prevPOS_C = Connectives_dict().dict_prevPOS_C
    # dict_self_category_to_root_path = Connectives_dict().dict_self_category_to_root_path
    dict_CParent_to_root_path_node_names = Connectives_dict().dict_CParent_to_root_path_node_names
    dict_conn_connCtx = Connectives_dict().dict_conn_connCtx
    dict_conn_rightSiblingCtx = Connectives_dict().dict_conn_rightSiblingCtx
    # dict_conn_leftSiblingCtx = Connectives_dict().dict_conn_leftSiblingCtx
    # dict_conn_left_right_SiblingCtx = Connectives_dict().dict_conn_left_right_SiblingCtx
    dict_conn_parent_category_Ctx = Connectives_dict().dict_conn_parent_category_Ctx
    dict_rightSibling_production_rules = Connectives_dict().dict_rightSibling_production_rules

    ''' c pos '''
    pos_tag_list = []
    for conn_index in conn_indices:
        pos_tag_list.append(parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
    CPOS = "_".join(pos_tag_list)

    ''' prev '''
    flag = 0
    prev_index = conn_indices[0] - 1
    prev_sent_index = sent_index
    if prev_index < 0:
        prev_index = -1
        prev_sent_index -= 1
        if prev_sent_index < 0:
            flag = 1
    # 连接词的前面一个词
    if flag == 1 :
        prev = "NONE"
    else:
        prev = parse_dict[DocID]["sentences"][prev_sent_index]["words"][prev_index][0]

    ''' conn_name '''
    #获取连接词到名称
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])

    '''prevPOS'''
    if prev == "NONE":
        prevPOS = "NONE"
    else:
        prevPOS = parse_dict[DocID]["sentences"][prev_sent_index]["words"][prev_index][1]["PartOfSpeech"]

    '''next'''
    #获取该句子长度，该doc的总句子数
    sent_count = len(parse_dict[DocID]["sentences"])
    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

    flag = 0
    next_index = conn_indices[-1] + 1
    next_sent_index = sent_index
    if next_index >= sent_length:
        next_sent_index += 1
        next_index = 0
        if next_sent_index >= sent_count:
            flag = 1
    # 连接词的后面一个词
    if flag == 1:
        next = "NONE"
    else:
        next = parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][0]

    ''' next pos '''
    if next == "NONE":
        nextPOS = "NONE"
    else:
        nextPOS = parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]


    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)


    ''' c parent to root '''
    if syntax_tree.tree == None:
        cparent_to_root_path = "NONE_TREE"
    else:
        cparent_to_root_path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up
            cparent_to_root_path += syntax_tree.get_node_path_to_root(conn_parent_node) + "&"
        if cparent_to_root_path[-1] == "&":
            cparent_to_root_path = cparent_to_root_path[:-1]

    ''' compressed c parent to root '''
    if syntax_tree.tree == None:
        compressed_path = "NONE_TREE"
    else:
        compressed_path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up

            path = syntax_tree.get_node_path_to_root(conn_parent_node)

            compressed_path += util.get_compressed_path(path) + "&"

        if compressed_path[-1] == "&":
            compressed_path = compressed_path[:-1]

    ''' Pitler '''
    if syntax_tree.tree == None:
        self_category = "NONE_TREE"
    else:
        self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

    if syntax_tree.tree == None:
        parent_category = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        if parent_category_node == None:
            parent_category = "ROOT"
        else:
            parent_category = parent_category_node.name

    if syntax_tree.tree == None:
        left_sibling_category = "NONE_TREE"
    else:
        left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        if left_sibling_category_node == None:
            left_sibling_category = "NONE"
        else:
            left_sibling_category = left_sibling_category_node.name

    if syntax_tree.tree == None:
        right_sibling_category = "NONE_TREE"
    else:
        right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        if right_sibling_category_node == None:
            right_sibling_category = "NONE"
        else:
            right_sibling_category = right_sibling_category_node.name


    prev_C = "%s|%s" % (prev, conn_name)
    prePOS_CPOS = "%s|%s" % (prevPOS, CPOS)
    C_next = "%s|%s" % (conn_name, next)
    CPOS_nextPOS = "%s|%s" % (CPOS, nextPOS)

    conn_self_category = "%s|%s" % (conn_name, self_category)
    conn_parent_category = "%s|%s" % (conn_name, parent_category)
    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)
    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

    self_parent = "%s|%s" % (self_category, parent_category)
    self_right = "%s|%s" % (self_category, right_sibling_category)
    self_left = "%s|%s" % (self_category, left_sibling_category)
    parent_left = "%s|%s" % (parent_category, left_sibling_category)
    parent_right = "%s|%s" % (parent_category, right_sibling_category)
    left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

    '''--- mine ---'''
    conn_lower_case = conn_name.lower()
    # prevPOS_C = "%s|%s" % (prevPOS, conn_name.lower())
    if syntax_tree.tree == None:
        _path = "NONE_TREE"
    else:
        _path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up
            _path += syntax_tree.get_node_path_to_root(conn_parent_node) + "-->"
        if _path[-3:] == "-->":
            _path = _path[:-3]

    # conn + connCtx
    if syntax_tree.tree == None:
        connCtx = "NONE_TREE"
    else:
        conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
        connCtx = dict_util.get_node_Ctx(conn_node, syntax_tree)

    conn_connCtx = "%s|%s" % (conn_name, connCtx)

    # conn + right sibling ctx
    if syntax_tree.tree == None:
        rightSiblingCtx = "NONE_TREE"
    else:
        rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        rightSiblingCtx = dict_util.get_node_linked_Ctx(rightSibling_node, syntax_tree)

    conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

    # conn _ left sibling ctx
    if syntax_tree.tree == None:
        leftSiblingCtx = "NONE_TREE"
    else:
        leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        leftSiblingCtx = dict_util.get_node_linked_Ctx(leftSibling_node, syntax_tree)

    conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

    # conn left right sibling ctx
    conn_left_right_SiblingCtx = "%s|%s|%s" % (conn_name, leftSiblingCtx, rightSiblingCtx)

    # conn parent category ctx
    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = dict_util.get_node_linked_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    #dict_conn_rightSibling_production_rules
    # if syntax_tree.tree == None:
    #     rightSibling_production_rules = ["NONE_TREE"]
    # else:
    #     rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
    #     rightSibling_production_rules = dict_util.get_node_production_rules(rightSibling_node, syntax_tree)


    features = []
    '''Z.Lin'''
    features.append(get_feature(feat_dict_CPOS_dict, CPOS_dict, CPOS))
    features.append(get_feature(feat_dict_prev_C_dict, prev_C_dict, prev_C))
    features.append(get_feature(feat_dict_prevPOS_dict, prevPOS_dict, prevPOS))
    features.append(get_feature(feat_dict_prevPOS_CPOS_dict, prevPOS_CPOS_dict, prePOS_CPOS ))
    features.append(get_feature(feat_dict_C_next_dict, C_next_dict, C_next))
    features.append(get_feature(feat_dict_nextPOS_dict, nextPOS_dict, nextPOS))
    features.append(get_feature(feat_dict_CPOS_nextPOS_dict, CPOS_nextPOS_dict, CPOS_nextPOS))
    features.append(get_feature(feat_dict_CParent_to_root_path_dict,CParent_to_root_path_dict, cparent_to_root_path ))
    features.append(get_feature(feat_dict_compressed_CParent_to_root_path_dict, compressed_CParent_to_root_path_dict, compressed_path))

    ''' pitler '''
    features.append(get_feature(feat_dict_self_category_dict, self_category_dict, self_category))
    features.append(get_feature(feat_dict_parent_category_dict, parent_category_dict, parent_category))
    features.append(get_feature(feat_dict_left_sibling_category_dict, left_sibling_category_dict, left_sibling_category))
    features.append(get_feature(feat_dict_right_sibling_category_dict, right_sibling_category_dict, right_sibling_category))

    feat_dict_is_right_sibling_contains_VP = {}
    if syntax_tree.tree != None and right_sibling_category_node != None:
        T = right_sibling_category_node.get_descendants()
        T.append(right_sibling_category_node)
        for node in T:
            if node.name == "VP" or node.name == "S":
                feat_dict_is_right_sibling_contains_VP[1] = 1
                break
    features.append(Feature("", 1, feat_dict_is_right_sibling_contains_VP))

    ''' conn-syn '''
    features.append(get_feature(feat_dict_conn_self_category_dict, conn_self_category_dict, conn_self_category))
    features.append(get_feature(feat_dict_conn_parent_category_dict, conn_parent_category_dict, conn_parent_category))
    features.append(get_feature(feat_dict_conn_left_sibling_category_dict, conn_left_sibling_category_dict, conn_left_sibling_category))
    features.append(get_feature(feat_dict_conn_right_sibling_category_dict, conn_right_sibling_category_dict, conn_right_sibling_category))

    ''' syn-syn '''

    features.append(get_feature(feat_dict_self_parent, self_parent_dict, self_parent))
    features.append(get_feature(feat_dict_self_right,self_right_dict, self_right ))
    features.append(get_feature(feat_dict_self_left, self_left_dict, self_left))
    features.append(get_feature(feat_dict_parent_left, parent_left_dict, parent_left))
    features.append(get_feature(feat_dict_parent_right, parent_right_dict, parent_right))
    features.append(get_feature(feat_dict_left_right,left_right_dict, left_right))

    ''' mine '''
    features.append(get_feature_by_feat(dict_conn_lower_case, conn_lower_case))
    features.append(get_feature_by_feat(dict_conn, conn_name))
    # features.append(get_feature_by_feat(dict_prevPOS_C, prevPOS_C))
    # features.append(get_feature_by_feat(dict_self_category_to_root_path, self_category_to_root_path))

    features.append(get_feature_by_feat_list(dict_CParent_to_root_path_node_names, _path.split("-->")))
    # features.append(get_feature_by_feat(dict_conn_connCtx, conn_connCtx))
    features.append(get_feature_by_feat(dict_conn_rightSiblingCtx, conn_rightSiblingCtx))
    # features.append(get_feature_by_feat(dict_conn_leftSiblingCtx, conn_leftSiblingCtx))
    # features.append(get_feature_by_feat(dict_conn_left_right_SiblingCtx, conn_left_right_SiblingCtx))
    features.append(get_feature_by_feat(dict_conn_parent_category_Ctx, conn_parent_categoryCtx))
    # features.append(get_feature_by_feat_list(dict_rightSibling_production_rules, rightSibling_production_rules))





    return util.mergeFeatures(features)


def get_feature(feat_dict, dict, feat):
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_list(list):
    feat_dict = {}
    for index, item in enumerate(list):
        if item != 0:
            feat_dict[index+1] = item
    return Feature("", len(list), feat_dict)


def get_feature_by_feat(dict, feat):
    feat_dict = {}
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_feat_list(dict, feat_list):
    feat_dict = {}
    for feat in feat_list:
        if feat in dict:
            feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)


