#coding:utf-8
from feature import Feature
import util
from explicit_dict import Explicit_dict
import exp_dict_util as dict_util
from syntax_tree import Syntax_tree


def all_features(parse_dict, connective):
    ''' feat dict '''
    feat_dict_CString = {}
    feat_dict_CPOS = {}
    feat_dict_C_Prev = {}


    ''' load dict '''
    dict_CString = Explicit_dict().dict_CString
    dict_CPOS = Explicit_dict().dict_CPOS
    dict_C_Prev = Explicit_dict().dict_C_Prev
    dict_CLString = Explicit_dict().dict_CLString

    '''Pitler'''
    self_category_dict = Explicit_dict().self_category_dict
    parent_category_dict = Explicit_dict().parent_category_dict
    left_sibling_category_dict = Explicit_dict().left_sibling_category_dict
    right_sibling_category_dict = Explicit_dict().right_sibling_category_dict
    ''' conn_syn '''
    conn_self_category_dict = Explicit_dict().conn_self_category_dict
    conn_parent_category_dict = Explicit_dict().conn_parent_category_dict
    conn_left_sibling_category_dict = Explicit_dict().conn_left_sibling_category_dict
    conn_right_sibling_category_dict = Explicit_dict().conn_right_sibling_category_dict
    ''' syn-syn'''
    self_parent_dict = Explicit_dict().self_parent_dict
    self_right_dict = Explicit_dict().self_right_dict
    self_left_dict = Explicit_dict().self_left_dict
    parent_left_dict = Explicit_dict().parent_left_dict
    parent_right_dict = Explicit_dict().parent_right_dict
    left_right_dict = Explicit_dict().left_right_dict

    ''' mine '''
    dict_conn_to_root_path = Explicit_dict().dict_conn_to_root_path
    dict_conn_next = Explicit_dict().dict_conn_next
    dict_conn_connCtx = Explicit_dict().dict_conn_connCtx
    dict_conn_rightSiblingCtx = Explicit_dict().dict_conn_rightSiblingCtx
    dict_conn_parent_category_ctx = Explicit_dict().dict_conn_parent_category_ctx
    dict_conn_leftSibling_ctx = Explicit_dict().dict_conn_leftSibling_ctx
    dict_CParent_to_root_path_node_names = Explicit_dict().dict_CParent_to_root_path_node_names
    dict_conn_parent_category_not_linked_ctx = Explicit_dict().dict_conn_parent_category_not_linked_ctx
    dict_conn_prev_conn = Explicit_dict().dict_conn_prev_conn
    dict_prev_conn = Explicit_dict().dict_prev_conn
    dict_as_prev_conn = Explicit_dict().dict_as_prev_conn
    dict_as_prev_connPOS = Explicit_dict().dict_as_prev_connPOS

    dict_when_prev_conn = Explicit_dict().dict_when_prev_conn
    dict_when_prev_connPOS = Explicit_dict().dict_when_prev_connPOS

    dict_as_before_after_tense = Explicit_dict().dict_as_before_after_tense
    dict_is_as_before_after_same_tense = {"YES": 1, "NO": 2, "NOT_as": 3}

    dict_when_is_contain_status = {"YES": 1, "NO": 2, "NOT_when": 3}

    dict_when_before_after_tense = Explicit_dict().dict_when_before_after_tense
    dict_when_after_lemma_verbs = Explicit_dict().dict_when_after_lemma_verbs

    ''' feature '''
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CPOS = dict_util.get_CPOS(parse_dict, DocID, sent_index, conn_indices)
    prev = dict_util.get_prev1(parse_dict, DocID, sent_index, conn_indices)
    C_Prev = "%s|%s" % (CString, prev)
    CLString = CString.lower()

    # syntax tree
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    #pitler
    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)
    #conn - syn
    conn_name = CLString
    conn_self_category = "%s|%s" % (conn_name, self_category)
    conn_parent_category = "%s|%s" % (conn_name, parent_category)
    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)
    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

    #syn-syn
    self_parent = "%s|%s" % (self_category, parent_category)
    self_right = "%s|%s" % (self_category, right_sibling_category)
    self_left = "%s|%s" % (self_category, left_sibling_category)
    parent_left = "%s|%s" % (parent_category, left_sibling_category)
    parent_right = "%s|%s" % (parent_category, right_sibling_category)
    left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

    ''' mine '''
    # conn_to_root_path = dict_util.get_conn_to_root_path(parse_dict, DocID, sent_index, conn_indices)
    # conn_next = dict_util.get_conn_next(parse_dict, DocID, sent_index, conn_indices)
    # conn_connCtx = dict_util.get_conn_connCtx(parse_dict, DocID, sent_index, conn_indices)
    # conn_rightSiblingCtx = dict_util.get_conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices)
    conn_parent_category_ctx = dict_util.get_conn_parent_category_Ctx(parse_dict, DocID, sent_index, conn_indices)
    # conn_leftSibling_ctx = dict_util.get_conn_leftSibling_ctx(parse_dict, DocID, sent_index, conn_indices)
    # CParent_to_root_path_node_names = dict_util.get_CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices)
    # conn_parent_category_not_linked_ctx = dict_util.get_conn_parent_category_not_linked_Ctx(parse_dict, DocID, sent_index, conn_indices)
    # conn_prev_conn = dict_util.get_conn_prev_conn(parse_dict, DocID, sent_index, conn_indices)
    # prev_conn = dict_util.get_prev_conn(parse_dict, DocID, sent_index, conn_indices)
    as_prev_conn = dict_util.get_as_prev_conn(parse_dict, DocID, sent_index, conn_indices)
    as_prev_connPOS = dict_util.get_as_prev_connPOS(parse_dict, DocID, sent_index, conn_indices)

    when_prev_conn = dict_util.get_when_prev_conn(parse_dict, DocID, sent_index, conn_indices)
    when_prev_connPOS = dict_util.get_when_prev_connPOS(parse_dict, DocID, sent_index, conn_indices)

    # as_before_after_tense = dict_util.get_as_before_after_tense(parse_dict, DocID, sent_index, conn_indices)
    # is_as_before_after_same_tense = dict_util.get_is_as_before_after_same_tense(parse_dict, DocID, sent_index, conn_indices)

    # when_is_contain_status = dict_util.get_when_is_contain_status(parse_dict, DocID, sent_index, conn_indices)

    # when_before_after_tense = dict_util.get_when_before_after_tense(parse_dict, DocID, sent_index, conn_indices)
    # when_after_lemma_verbs = dict_util.get_when_after_lemma_verbs(parse_dict, DocID, sent_index, conn_indices)

    features = []
    features.append(get_feature(feat_dict_CString, dict_CString , CString))
    features.append(get_feature(feat_dict_CPOS, dict_CPOS , CPOS))
    features.append(get_feature(feat_dict_C_Prev, dict_C_Prev , C_Prev))
    features.append(get_feature({}, dict_CLString , CLString))


    features.append(get_feature({}, self_category_dict , self_category))
    features.append(get_feature({}, parent_category_dict , parent_category))
    features.append(get_feature({}, left_sibling_category_dict , left_sibling_category))
    features.append(get_feature({}, right_sibling_category_dict , right_sibling_category))


    features.append(get_feature({}, conn_self_category_dict , conn_self_category))
    features.append(get_feature({}, conn_parent_category_dict , conn_parent_category))
    features.append(get_feature({}, conn_left_sibling_category_dict , conn_left_sibling_category))
    features.append(get_feature({}, conn_right_sibling_category_dict , conn_right_sibling_category))

    features.append(get_feature({}, self_parent_dict, self_parent))
    features.append(get_feature({}, self_right_dict, self_right ))
    features.append(get_feature({}, self_left_dict, self_left))
    features.append(get_feature({}, parent_left_dict, parent_left))
    features.append(get_feature({}, parent_right_dict, parent_right))
    features.append(get_feature({}, left_right_dict, left_right))

    ''' mine '''
    # features.append(get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path))
    # features.append(get_feature_by_feat(dict_conn_next, conn_next))
    # features.append(get_feature_by_feat(dict_conn_connCtx, conn_connCtx))
    # features.append(get_feature_by_feat(dict_conn_rightSiblingCtx, conn_rightSiblingCtx))
    features.append(get_feature_by_feat(dict_conn_parent_category_ctx, conn_parent_category_ctx))
    # features.append(get_feature_by_feat(dict_conn_leftSibling_ctx, conn_leftSibling_ctx))
    # features.append(get_feature_by_feat_list(dict_CParent_to_root_path_node_names, CParent_to_root_path_node_names))
    # features.append(get_feature_by_feat(dict_conn_parent_category_not_linked_ctx, conn_parent_category_not_linked_ctx))
    # features.append(get_feature_by_feat(dict_conn_prev_conn, conn_prev_conn))
    # features.append(get_feature_by_feat(dict_prev_conn, prev_conn))
    features.append(get_feature_by_feat(dict_as_prev_conn, as_prev_conn))
    features.append(get_feature_by_feat(dict_as_prev_connPOS, as_prev_connPOS))

    features.append(get_feature_by_feat(dict_when_prev_conn, when_prev_conn))
    features.append(get_feature_by_feat(dict_when_prev_connPOS, when_prev_connPOS))

    # features.append(get_feature_by_feat(dict_as_before_after_tense, as_before_after_tense))
    # features.append(get_feature_by_feat(dict_is_as_before_after_same_tense, is_as_before_after_same_tense))

    # features.append(get_feature_by_feat(dict_when_is_contain_status, when_is_contain_status))

    # features.append(get_feature_by_feat(dict_when_before_after_tense, when_before_after_tense))
    # features.append(get_feature_by_feat(dict_when_after_lemma_verbs, when_after_lemma_verbs))

    return util.mergeFeatures(features)



def _all_features(parse_dict, connective):
    DocID = connective.DocID
    sent_index = connective.sent_index
    conn_indices = connective.token_indices

    feature_function_list = [
        # Z.lin
        CString,
        CPOS,
        C_Prev,
        CLString,
        # Pitler
        self_category,
        parent_category,
        left_sibling_category,
        right_sibling_category,
        # conn - syn
        conn_self_category,
        conn_parent_category,
        conn_left_sibling_category,
        conn_right_sibling_category,
        # syn - syn
        self_parent,
        self_right,
        self_left,
        parent_left,
        parent_right,
        left_right,
        # mine
        conn_parent_category_ctx,
        as_prev_conn,
        as_prev_connPOS,
        when_prev_conn,
        when_prev_connPOS

    ]

    features = [feature_function(parse_dict, DocID, sent_index, conn_indices) for feature_function in feature_function_list]
    # merge features
    feature = util.mergeFeatures(features)
    return feature

def CString(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_CString = Explicit_dict().dict_CString
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_CString, CString)

def CPOS(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_CPOS = Explicit_dict().dict_CPOS
    # feature
    CPOS = dict_util.get_CPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_CPOS, CPOS)

def C_Prev(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_C_Prev = Explicit_dict().dict_C_Prev
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    prev = dict_util.get_prev1(parse_dict, DocID, sent_index, conn_indices)
    C_Prev = "%s|%s" % (CString, prev)

    return get_feature_by_feat(dict_C_Prev, C_Prev)

def CLString(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_CLString = Explicit_dict().dict_CLString
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()

    return get_feature_by_feat(dict_CLString, CLString)

def self_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    self_category_dict = Explicit_dict().self_category_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)

    return get_feature_by_feat(self_category_dict, self_category)

def parent_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    parent_category_dict = Explicit_dict().parent_category_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    #pitler
    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)

    return get_feature_by_feat(parent_category_dict, parent_category)

def left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    left_sibling_category_dict = Explicit_dict().left_sibling_category_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)

    return get_feature_by_feat(left_sibling_category_dict, left_sibling_category)

def right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    right_sibling_category_dict = Explicit_dict().right_sibling_category_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    #pitler
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)

    return get_feature_by_feat(right_sibling_category_dict, right_sibling_category)

def conn_syn(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    conn_self_category_dict = Explicit_dict().conn_self_category_dict
    conn_parent_category_dict = Explicit_dict().conn_parent_category_dict
    conn_left_sibling_category_dict = Explicit_dict().conn_left_sibling_category_dict
    conn_right_sibling_category_dict = Explicit_dict().conn_right_sibling_category_dict

    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)

    conn_name = CLString
    conn_self_category = "%s|%s" % (conn_name, self_category)
    conn_parent_category = "%s|%s" % (conn_name, parent_category)
    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)
    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

    features = []
    features.append(get_feature_by_feat(conn_self_category_dict , conn_self_category))
    features.append(get_feature_by_feat(conn_parent_category_dict , conn_parent_category))
    features.append(get_feature_by_feat(conn_left_sibling_category_dict , conn_left_sibling_category))
    features.append(get_feature_by_feat(conn_right_sibling_category_dict , conn_right_sibling_category))

    return util.mergeFeatures(features)

def syn_syn(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    self_parent_dict = Explicit_dict().self_parent_dict
    self_right_dict = Explicit_dict().self_right_dict
    self_left_dict = Explicit_dict().self_left_dict
    parent_left_dict = Explicit_dict().parent_left_dict
    parent_right_dict = Explicit_dict().parent_right_dict
    left_right_dict = Explicit_dict().left_right_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)

    self_parent = "%s|%s" % (self_category, parent_category)
    self_right = "%s|%s" % (self_category, right_sibling_category)
    self_left = "%s|%s" % (self_category, left_sibling_category)
    parent_left = "%s|%s" % (parent_category, left_sibling_category)
    parent_right = "%s|%s" % (parent_category, right_sibling_category)
    left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

    features = []
    features.append(get_feature_by_feat(self_parent_dict, self_parent))
    features.append(get_feature_by_feat(self_right_dict, self_right ))
    features.append(get_feature_by_feat(self_left_dict, self_left))
    features.append(get_feature_by_feat(parent_left_dict, parent_left))
    features.append(get_feature_by_feat(parent_right_dict, parent_right))
    features.append(get_feature_by_feat(left_right_dict, left_right))

    return util.mergeFeatures(features)

def conn_self_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    conn_self_category_dict = Explicit_dict().conn_self_category_dict
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()
    conn_name = CLString
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)

    conn_self_category = "%s|%s" % (conn_name, self_category)

    return get_feature_by_feat(conn_self_category_dict , conn_self_category)

def conn_parent_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    conn_parent_category_dict = Explicit_dict().conn_parent_category_dict
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()
    conn_name = CLString

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)

    conn_parent_category = "%s|%s" % (conn_name, parent_category)

    return get_feature_by_feat(conn_parent_category_dict , conn_parent_category)

def conn_left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    conn_left_sibling_category_dict = Explicit_dict().conn_left_sibling_category_dict
    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()
    conn_name = CLString

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)

    conn_left_sibling_category = "%s|%s" % (conn_name, left_sibling_category)

    return get_feature_by_feat(conn_left_sibling_category_dict , conn_left_sibling_category)

def conn_right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    conn_right_sibling_category_dict = Explicit_dict().conn_right_sibling_category_dict

    # feature
    CString = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CLString = CString.lower()
    conn_name = CLString

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)
    conn_right_sibling_category = "%s|%s" % (conn_name, right_sibling_category)

    return get_feature_by_feat(conn_right_sibling_category_dict , conn_right_sibling_category)

def self_parent(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    self_parent_dict = Explicit_dict().self_parent_dict

    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)

    self_parent = "%s|%s" % (self_category, parent_category)

    features = []
    features.append(get_feature_by_feat(self_parent_dict, self_parent))

    return util.mergeFeatures(features)

def self_right(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    self_right_dict = Explicit_dict().self_right_dict

    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)


    self_right = "%s|%s" % (self_category, right_sibling_category)


    features = []

    features.append(get_feature_by_feat(self_right_dict, self_right ))


    return util.mergeFeatures(features)

def self_left(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    self_left_dict = Explicit_dict().self_left_dict

    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    self_category = dict_util.get_self_category(syntax_tree, conn_indices)
    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)


    self_left = "%s|%s" % (self_category, left_sibling_category)


    features = []

    features.append(get_feature_by_feat(self_left_dict, self_left))

    return util.mergeFeatures(features)

def parent_left(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    parent_left_dict = Explicit_dict().parent_left_dict

    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)


    parent_left = "%s|%s" % (parent_category, left_sibling_category)

    features = []

    features.append(get_feature_by_feat(parent_left_dict, parent_left))


    return util.mergeFeatures(features)

def parent_right(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    parent_right_dict = Explicit_dict().parent_right_dict

    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    parent_category = dict_util.get_parent_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)


    parent_right = "%s|%s" % (parent_category, right_sibling_category)


    features = []

    features.append(get_feature_by_feat(parent_right_dict, parent_right))


    return util.mergeFeatures(features)

def left_right(parse_dict, DocID, sent_index, conn_indices):
    # load dict

    left_right_dict = Explicit_dict().left_right_dict
    # feature
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    left_sibling_category = dict_util.get_left_sibling_category(syntax_tree, conn_indices)
    right_sibling_category = dict_util.get_right_sibling_category(syntax_tree, conn_indices)


    left_right = "%s|%s" % (left_sibling_category, right_sibling_category)

    features = []

    features.append(get_feature_by_feat(left_right_dict, left_right))

    return util.mergeFeatures(features)

def conn_parent_category_ctx(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_conn_parent_category_ctx = Explicit_dict().dict_conn_parent_category_ctx
    # feature
    conn_parent_category_ctx = dict_util.get_conn_parent_category_Ctx(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_conn_parent_category_ctx, conn_parent_category_ctx)

def as_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_as_prev_conn = Explicit_dict().dict_as_prev_conn
    # feature
    as_prev_conn = dict_util.get_as_prev_conn(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_as_prev_conn, as_prev_conn)

def as_prev_connPOS(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_as_prev_connPOS = Explicit_dict().dict_as_prev_connPOS
    # feature
    as_prev_connPOS = dict_util.get_as_prev_connPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_as_prev_connPOS, as_prev_connPOS)

def when_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_when_prev_conn = Explicit_dict().dict_when_prev_conn
    # feature
    when_prev_conn = dict_util.get_when_prev_conn(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_when_prev_conn, when_prev_conn)

def when_prev_connPOS(parse_dict, DocID, sent_index, conn_indices):
    # load dict
    dict_when_prev_connPOS = Explicit_dict().dict_when_prev_connPOS
    # feature
    when_prev_connPOS = dict_util.get_when_prev_connPOS(parse_dict, DocID, sent_index, conn_indices)

    return get_feature_by_feat(dict_when_prev_connPOS, when_prev_connPOS)






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