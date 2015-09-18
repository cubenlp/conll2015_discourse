#coding:utf-8
from feature import Feature
import util
from NT_dict import NT_dict
import NT_dict_util as dict_util
from syntax_tree import Syntax_tree
from constituent import Constituent
from connective_dict import Connectives_dict

dict_clauses = {}

def all_features(parse_dict, constituent, i, constituents):

    syntax_tree = constituent.syntax_tree
    conn_category = Connectives_dict().conn_category
    connective = constituent.connective

    ''' feat dict '''
    feat_dict_CON_Str = {}
    feat_dict_CON_LStr = {}
    feat_dict_NT_Ctx = {}
    feat_dict_CON_NT_Path = {}
    feat_dict_CON_NT_Path_iLsib = {}



    ''' load dict '''
    dict_CON_Str = NT_dict().dict_CON_Str
    dict_CON_LStr = NT_dict().dict_CON_LStr
    dict_NT_Ctx = NT_dict().dict_NT_Ctx
    dict_CON_NT_Path = NT_dict().dict_CON_NT_Path
    dict_CON_NT_Path_iLsib = NT_dict().dict_CON_NT_Path_iLsib


    dict_NT_prev_curr_Path = NT_dict().dict_NT_prev_curr_Path
    dict_CON_POS = NT_dict().dict_CON_POS
    dict_C_Prev = NT_dict().dict_C_Prev
    dict_NT_Name = NT_dict().dict_NT_Name

    dict_NT_prev_curr_production_rule = NT_dict().dict_NT_prev_curr_production_rule

    dict_nt_ntParent_ctx = NT_dict().dict_nt_ntParent_ctx

    ''' feature '''
    #获取该句话的语法树
    conn_indices = connective.token_indices
    DocID = connective.DocID
    sent_index = connective.sent_index

    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_Str = dict_util.get_CON_Str(parse_dict, DocID, sent_index, conn_indices)
    CON_LStr = CON_Str.lower()
    CON_Cat = conn_category[connective.name]
    CON_iLSib = dict_util.get_CON_iLSib(syntax_tree,conn_node)
    CON_iRSib = dict_util.get_CON_iRSib(syntax_tree,conn_node)
    NT_Ctx = dict_util.get_NT_Ctx(constituent)
    CON_NT_Path = dict_util.get_CON_NT_Path(conn_node, constituent)
    CON_NT_Position = dict_util.get_CON_NT_Position(conn_node, constituent)
    if CON_iLSib > 1:
        CON_NT_Path_iLsib = CON_NT_Path + ":>1"
    else:
        CON_NT_Path_iLsib = CON_NT_Path + ":<=1"


    ''' test new '''
    NT_prev_curr_Path = dict_util.get_NT_prev_curr_Path(i, constituents)

    # SABR_anc = dict_util.has_SBAR_ancestor(constituent)
    # if SABR_anc:
    #     SABR_feat = 1
    # else:
    #     SABR_feat = 0

    # if (DocID, sent_index) not in dict_clauses:
    #     clauses_list = dict_util.get_sent_clauses(parse_dict, DocID, sent_index)
    #     dict_clauses[(DocID, sent_index)] = clauses_list
    #
    # clauses_list = dict_clauses[(DocID, sent_index)]#[[1,2],[4,5,6]]
    # #为每个constituent ,判断她是否与前面的一个constituent是否处于同一个clause
    # prev_curr_some_clause = 0
    # if i > 0:
    #     curr_clause_NO = -1
    #     for k, item in enumerate(clauses_list):
    #         if set(constituents[i].indices) <= set(item):
    #             curr_clause_NO = k
    #             break
    #     prev_clause_NO = -1
    #     for k, item in enumerate(clauses_list):
    #         if set(constituents[i - 1].indices) <= set(item):
    #             prev_clause_NO = k
    #             break
    #
    #     if curr_clause_NO != -1 and prev_clause_NO != -1 and curr_clause_NO == prev_clause_NO:
    #         prev_curr_some_clause = 1
    #
    # CON_POS = dict_util.get_CON_POS(parse_dict, DocID, sent_index, conn_indices)


    # nt_ntParent_ctx = dict_util.get_NT_NTparent_Ctx(constituent)


    # prev = dict_util.get_prev1(parse_dict, DocID, sent_index, conn_indices)
    # C_Prev = "%s|%s" % (CON_Str, prev)
    #
    # NT_Name = constituent.node.name
    #
    # NT_prev_curr_production_rule = dict_util.get_NT_prev_curr_production_rule(i, constituents)

    features = []
    features.append(get_feature(feat_dict_CON_Str, dict_CON_Str , CON_Str))
    features.append(get_feature(feat_dict_CON_LStr, dict_CON_LStr, CON_LStr))
    features.append(get_feature(feat_dict_NT_Ctx, dict_NT_Ctx, NT_Ctx))
    features.append(get_feature(feat_dict_CON_NT_Path, dict_CON_NT_Path, CON_NT_Path))
    features.append(get_feature(feat_dict_CON_NT_Path_iLsib, dict_CON_NT_Path_iLsib, CON_NT_Path_iLsib))
    # cat
    dict_category = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }
    features.append(get_feature({}, dict_category , CON_Cat))
    #number
    features.append(Feature("", 1, {1: CON_iLSib}))
    features.append(Feature("", 1, {1: CON_iRSib}))
    #position
    dict_position = {"right": 1, "left": 2}
    features.append(get_feature({}, dict_position , CON_NT_Position))

    #NT_prev_curr_Path
    # features.append(get_feature({}, dict_NT_prev_curr_Path , NT_prev_curr_Path))
    # features.append(Feature("", 1, {1: SABR_feat}))
    # features.append(Feature("", 1, {1: prev_curr_some_clause}))
    # features.append(Feature("", 1, {1: curr_clause_NO}))

    # features.append(get_feature({}, dict_CON_POS, CON_POS))
    # features.append(get_feature({}, dict_C_Prev, C_Prev))
    # features.append(get_feature({}, dict_NT_Name, NT_Name))

    # features.append(get_feature({}, dict_NT_prev_curr_production_rule, NT_prev_curr_production_rule))

    # features.append(get_feature_by_feat(dict_nt_ntParent_ctx, nt_ntParent_ctx))

    return util.mergeFeatures(features)


def _all_features(parse_dict, constituent, i, constituents):
    feature_function_list = [
        CON_POS,


        NT_prev_curr_Path,
        CParent_to_root_path,
        self_category,


        CParent_to_root_path_node_names,
        left_sibling_category,
        NT_to_root_path,
        conn_parent_categoryCtx,
        parent_category,
        conn_rightSiblingCtx,


        CON_Str,
        CON_LStr,
        CON_Cat,
        CON_iRSib,

        NT_Ctx,
        CON_NT_Path,
        CON_NT_Path_iLsib,

    ]

    features = [feature_function(parse_dict, constituent, i, constituents) for feature_function in feature_function_list]
    #合并特征
    feature = util.mergeFeatures(features)
    return feature


def CON_Str(parse_dict, constituent, i, constituents):
    # load dict
    dict_CON_Str = NT_dict().dict_CON_Str
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices
    CON_Str = dict_util.get_CON_Str(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_CON_Str, CON_Str)

def CON_LStr(parse_dict, constituent, i, constituents):
    # load dict
    dict_CON_LStr = NT_dict().dict_CON_LStr
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices
    CON_Str = dict_util.get_CON_Str(parse_dict, DocID, sent_index, conn_indices)

    CON_LStr = CON_Str.lower()

    return get_feature_by_feat(dict_CON_LStr, CON_LStr)

def CON_Cat(parse_dict, constituent, i, constituents):
    # load dict
    dict_category = {"subordinator": 1, "coordinator": 2, "adverbial": 3 }
    # 特征
    conn_category = Connectives_dict().conn_category
    connective = constituent.connective
    CON_Cat = conn_category[connective.name]

    return get_feature_by_feat(dict_category, CON_Cat)

def CON_iLSib(parse_dict, constituent, i, constituents):
    # 特征
    syntax_tree = constituent.syntax_tree
    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_iLSib = dict_util.get_CON_iLSib(syntax_tree, conn_node)

    return Feature("", 1, {1: CON_iLSib})

def CON_iRSib(parse_dict, constituent, i, constituents):
    # 特征
    syntax_tree = constituent.syntax_tree
    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_iRSib = dict_util.get_CON_iRSib(syntax_tree, conn_node)

    return Feature("", 1, {1: CON_iRSib})

def NT_Ctx(parse_dict, constituent, i, constituents):
    # load dict
    dict_NT_Ctx = NT_dict().dict_NT_Ctx
    # 特征
    NT_Ctx = dict_util.get_NT_Ctx(constituent)

    return get_feature_by_feat(dict_NT_Ctx, NT_Ctx)

def CON_NT_Path(parse_dict, constituent, i, constituents):
    # load dict
    dict_CON_NT_Path = NT_dict().dict_CON_NT_Path
    # 特征
    syntax_tree = constituent.syntax_tree
    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_NT_Path = dict_util.get_CON_NT_Path(conn_node, constituent)

    return get_feature_by_feat(dict_CON_NT_Path, CON_NT_Path)

def CON_NT_Path_iLsib(parse_dict, constituent, i, constituents):
    # load dict
    dict_CON_NT_Path_iLsib = NT_dict().dict_CON_NT_Path_iLsib
    # 特征
    syntax_tree = constituent.syntax_tree
    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_NT_Path = dict_util.get_CON_NT_Path(conn_node, constituent)
    CON_iLSib = dict_util.get_CON_iLSib(syntax_tree, conn_node)

    if CON_iLSib > 1:
        CON_NT_Path_iLsib = CON_NT_Path + ":>1"
    else:
        CON_NT_Path_iLsib = CON_NT_Path + ":<=1"

    return get_feature_by_feat(dict_CON_NT_Path_iLsib, CON_NT_Path_iLsib)

def CON_NT_Position(parse_dict, constituent, i, constituents):
    # load dict
    dict_position = {"right": 1, "left": 2}
    # 特征
    syntax_tree = constituent.syntax_tree
    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    CON_NT_Position = dict_util.get_CON_NT_Position(conn_node, constituent)

    return get_feature_by_feat(dict_position, CON_NT_Position)

def NT_prev_curr_Path(parse_dict, constituent, i, constituents):
    # load dict
    dict_NT_prev_curr_Path = NT_dict().dict_NT_prev_curr_Path
    # 特征
    NT_prev_curr_Path = dict_util.get_NT_prev_curr_Path(i, constituents)

    return get_feature_by_feat(dict_NT_prev_curr_Path, NT_prev_curr_Path)

def prev_curr_some_clause(parse_dict, constituent, i, constituents):
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index

    if (DocID, sent_index) not in dict_clauses:
        clauses_list = dict_util.get_sent_clauses(parse_dict, DocID, sent_index)
        dict_clauses[(DocID, sent_index)] = clauses_list
    clauses_list = dict_clauses[(DocID, sent_index)]#[[1,2],[4,5,6]]
    #为每个constituent ,判断她是否与前面的一个constituent是否处于同一个clause
    prev_curr_some_clause = 0
    if i > 0:
        curr_clause_NO = -1
        for k, item in enumerate(clauses_list):
            if set(constituents[i].indices) <= set(item):
                curr_clause_NO = k
                break
        prev_clause_NO = -1
        for k, item in enumerate(clauses_list):
            if set(constituents[i - 1].indices) <= set(item):
                prev_clause_NO = k
                break

        if curr_clause_NO != -1 and prev_clause_NO != -1 and curr_clause_NO == prev_clause_NO:
            prev_curr_some_clause = 1

    return Feature("", 1, {1: prev_curr_some_clause})

def CON_POS(parse_dict, constituent, i, constituents):
    # load dict
    dict_CON_POS = NT_dict().dict_CON_POS
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    CON_POS = dict_util.get_CON_POS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_CON_POS, CON_POS)


def CParent_to_root_path(parse_dict, constituent, i, constituents):
    # load dict
    dict_CParent_to_root_path = NT_dict().dict_CParent_to_root_path
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    CParent_to_root_path = dict_util.get_CParent_to_root_path(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_CParent_to_root_path, CParent_to_root_path)

def CParent_to_root_path_node_names(parse_dict, constituent, i, constituents):
    # load dict
    dict_CParent_to_root_path_node_names = NT_dict().dict_CParent_to_root_path_node_names
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    CParent_to_root_path_node_names = dict_util.get_CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat_list(dict_CParent_to_root_path_node_names, CParent_to_root_path_node_names)

def conn_connCtx(parse_dict, constituent, i, constituents):
    # load dict
    dict_conn_connCtx = NT_dict().dict_conn_connCtx
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    conn_connCtx = dict_util.get_conn_connCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_connCtx, conn_connCtx)

def conn_parent_categoryCtx(parse_dict, constituent, i, constituents):
    # load dict
    dict_conn_parent_categoryCtx = NT_dict().dict_conn_parent_categoryCtx
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    conn_parent_categoryCtx = dict_util.get_conn_parent_categoryCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_parent_categoryCtx, conn_parent_categoryCtx)

def conn_rightSiblingCtx(parse_dict, constituent, i, constituents):
    # load dict
    dict_conn_rightSiblingCtx = NT_dict().dict_conn_rightSiblingCtx
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    conn_rightSiblingCtx = dict_util.get_conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_rightSiblingCtx, conn_rightSiblingCtx)

def self_category(parse_dict, constituent, i, constituents):
    # load dict
    dict_self_category = NT_dict().dict_self_category
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    self_category = dict_util.get_self_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_self_category, self_category)

def parent_category(parse_dict, constituent, i, constituents):
    # load dict
    dict_parent_category = NT_dict().dict_parent_category
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    parent_category = dict_util.get_parent_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_parent_category, parent_category)

def left_sibling_category(parse_dict, constituent, i, constituents):
    # load dict
    dict_left_sibling_category = NT_dict().dict_left_sibling_category
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    left_sibling_category = dict_util.get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_left_sibling_category, left_sibling_category)

def right_sibling_category(parse_dict, constituent, i, constituents):
    # load dict
    dict_right_sibling_category = NT_dict().dict_right_sibling_category
    # 特征
    connective = constituent.connective
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    right_sibling_category = dict_util.get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_right_sibling_category, right_sibling_category)

def NT_Linked_ctx(parse_dict, constituent, i, constituents):
    # load dict
    dict_NT_Linked_ctx = NT_dict().dict_NT_Linked_ctx
    # 特征
    NT_Linked_ctx = dict_util.get_NT_Linked_ctx(constituent)

    return get_feature_by_feat(dict_NT_Linked_ctx, NT_Linked_ctx)

def NT_to_root_path(parse_dict, constituent, i, constituents):
    # load dict
    dict_NT_to_root_path = NT_dict().dict_NT_to_root_path
    # 特征
    NT_to_root_path = dict_util.get_NT_to_root_path(constituent)

    return get_feature_by_feat(dict_NT_to_root_path, NT_to_root_path)

def NT_parent_linked_ctx(parse_dict, constituent, i, constituents):
    # load dict
    dict_NT_parent_linked_ctx = NT_dict().dict_NT_parent_linked_ctx
    # 特征
    NT_parent_linked_ctx = dict_util.get_NT_parent_linked_ctx(constituent)

    return get_feature_by_feat(dict_NT_parent_linked_ctx, NT_parent_linked_ctx)

def NT_iLSib(parse_dict, constituent, i, constituents):
    node = constituent.node
    syntax_tree = constituent.syntax_tree

    return Feature("", 1, {1: len(syntax_tree.get_left_siblings(node))})

def NT_iRSib(parse_dict, constituent, i, constituents):
    node = constituent.node
    syntax_tree = constituent.syntax_tree

    return Feature("", 1, {1: len(syntax_tree.get_right_siblings(node))})

def NT_conn_level_distance(parse_dict, constituent, i, constituents):
    syntax_tree = constituent.syntax_tree

    nt_node = constituent.node

    connective = constituent.connective
    conn_indices = connective.token_indices
    conn_node = dict_util.get_conn_node(syntax_tree, conn_indices)

    root_node = syntax_tree.tree.get_tree_root()

    nt_level = int(syntax_tree.tree.get_distance(root_node, nt_node))
    conn_level = int(syntax_tree.tree.get_distance(root_node, conn_node))

    return Feature("", 1, {1:  conn_level - nt_level})


def NT_prev_curr_level_distance(parse_dict, constituent, i, constituents):
    if i == 0:
        return Feature("", 1, {1: 100})

    curr = constituents[i].node
    prev = constituents[i - 1].node

    syntax_tree = constituent.syntax_tree
    root_node = syntax_tree.tree.get_tree_root()

    curr_level = int(syntax_tree.tree.get_distance(root_node, curr))
    prev_level = int(syntax_tree.tree.get_distance(root_node, prev))

    return Feature("", 1, {1: curr_level - prev_level})

def NT_curr_next_level_distance(parse_dict, constituent, i, constituents):
    if i == len(constituents) - 1:
        return Feature("", 1, {1: 100})

    curr = constituents[i].node
    next = constituents[i + 1].node

    syntax_tree = constituent.syntax_tree
    root_node = syntax_tree.tree.get_tree_root()

    curr_level = int(syntax_tree.tree.get_distance(root_node, curr))
    next_level = int(syntax_tree.tree.get_distance(root_node, next))

    return Feature("", 1, {1: next_level - curr_level})

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