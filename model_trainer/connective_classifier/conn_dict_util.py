#coding:utf-8
# self, parent, left, right
from syntax_tree import Syntax_tree
import util

def get_node_Ctx(node, syntax_tree):
    if node == None:
        return "None"
    Ctx = []
    #self
    Ctx.append(node.name)
    #parent
    if node.up == None:
        Ctx.append("NULL")
    else:
        Ctx.append(node.up.name)
    #left
    left_siblings = syntax_tree.get_left_siblings(node)
    if left_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(left_siblings[-1].name)
    #right
    right_siblings = syntax_tree.get_right_siblings(node)
    if right_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(right_siblings[0].name)

    nodeCtx = "-".join(Ctx)
    return nodeCtx

#与之相连的上下文
def get_node_linked_Ctx(node, syntax_tree):
    if node == None:
        return "None"
    Ctx = []
    #self
    Ctx.append(node.name)
    #parent
    if node.up == None:
        Ctx.append("NULL")
    else:
        Ctx.append(node.up.name)
    #children
    for child in node.get_children():
        Ctx.append(child.name)

    return "-".join(Ctx)

#node对应的子树的production rules
def get_node_production_rules(node, syntax_tree):
    if node == None:
        return ["None"]
    if node.is_leaf():
        return ["Leaf"]

    production_rules = []
    #层次遍历
    for T in node.traverse(strategy="levelorder"):
        if not T.is_leaf():
            rule = T.name + "-->" + " ".join([child.name for child in T.get_children()])
            production_rules.append(rule)
    return production_rules

def get_CPOS(parse_dict, DocID, sent_index, conn_indices):
    pos_tag_list = []
    for conn_index in conn_indices:
        pos_tag_list.append(parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
    CPOS = "_".join(pos_tag_list)

    return CPOS

def get_prev(parse_dict, DocID, sent_index, conn_indices):
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

    return prev

def get_conn_name(parse_dict, DocID, sent_index, conn_indices):
    ''' conn_name '''
    #获取连接词到名称
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name

def get_prevPOS(parse_dict, DocID, sent_index, conn_indices):
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
        prevPOS = "NONE"
    else:
        prevPOS = parse_dict[DocID]["sentences"][prev_sent_index]["words"][prev_index][1]["PartOfSpeech"]

    return prevPOS

def get_next(parse_dict, DocID, sent_index, conn_indices):
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

    return next

def get_nextPOS(parse_dict, DocID, sent_index, conn_indices):
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
        nextPOS = "NONE"
    else:
        nextPOS = parse_dict[DocID]["sentences"][next_sent_index]["words"][next_index][1]["PartOfSpeech"]

    return nextPOS

def get_CParent_to_root_path(parse_dict, DocID, sent_index, conn_indices):
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

    return cparent_to_root_path

def get_compressed_cparent_to_root_path(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

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

    return compressed_path

def get_self_category(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        self_category = "NONE_TREE"
    else:
        self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name

    return self_category

def get_parent_category(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        parent_category = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        if parent_category_node == None:
            parent_category = "ROOT"
        else:
            parent_category = parent_category_node.name

    return parent_category

def get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        left_sibling_category = "NONE_TREE"
    else:
        left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        if left_sibling_category_node == None:
            left_sibling_category = "NONE"
        else:
            left_sibling_category = left_sibling_category_node.name

    return left_sibling_category

def get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        right_sibling_category = "NONE_TREE"
    else:
        right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        if right_sibling_category_node == None:
            right_sibling_category = "NONE"
        else:
            right_sibling_category = right_sibling_category_node.name

    return right_sibling_category

def get_prev_C(parse_dict, DocID, sent_index, conn_indices):
    prev = get_prev(parse_dict, DocID, sent_index, conn_indices)
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (prev, conn_name)

def get_prePOS_CPOS(parse_dict, DocID, sent_index, conn_indices):
    prevPOS = get_prevPOS(parse_dict, DocID, sent_index, conn_indices)
    CPOS = get_CPOS(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (prevPOS, CPOS)

def get_C_next(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
    next = get_next(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (conn_name, next)

def get_CPOS_nextPOS(parse_dict, DocID, sent_index, conn_indices):
    CPOS = get_CPOS(parse_dict, DocID, sent_index, conn_indices)
    nextPOS = get_nextPOS(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (CPOS, nextPOS)

def get_conn_self_category(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
    self_category = get_self_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (conn_name, self_category)

def get_conn_parent_category(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
    parent_category = get_parent_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (conn_name, parent_category)

def get_conn_left_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
    left_sibling_category = get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (conn_name, left_sibling_category)

def get_conn_right_sibling_category(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
    right_sibling_category = get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (conn_name, right_sibling_category)

def get_self_parent(parse_dict, DocID, sent_index, conn_indices):
    self_category = get_self_category(parse_dict, DocID, sent_index, conn_indices)
    parent_category = get_parent_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (self_category, parent_category)

def get_self_right(parse_dict, DocID, sent_index, conn_indices):
    self_category = get_self_category(parse_dict, DocID, sent_index, conn_indices)
    right_sibling_category = get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (self_category, right_sibling_category)

def get_self_left(parse_dict, DocID, sent_index, conn_indices):
    self_category = get_self_category(parse_dict, DocID, sent_index, conn_indices)
    left_sibling_category = get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (self_category, left_sibling_category)

def get_parent_left(parse_dict, DocID, sent_index, conn_indices):
    parent_category = get_parent_category(parse_dict, DocID, sent_index, conn_indices)
    left_sibling_category = get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (parent_category, left_sibling_category)

def get_parent_right(parse_dict, DocID, sent_index, conn_indices):
    parent_category = get_parent_category(parse_dict, DocID, sent_index, conn_indices)
    right_sibling_category = get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (parent_category, right_sibling_category)

def get_left_right(parse_dict, DocID, sent_index, conn_indices):
    left_sibling_category = get_left_sibling_category(parse_dict, DocID, sent_index, conn_indices)
    right_sibling_category = get_right_sibling_category(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (left_sibling_category, right_sibling_category)


def get_conn_lower_case(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    return conn_name.lower()

def get_CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices):
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        path = "NONE_TREE"
    else:
        path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            conn_parent_node = conn_node.up
            path += syntax_tree.get_node_path_to_root(conn_parent_node) + "-->"
        if path[-3:] == "-->":
            path = path[:-3]

    return path.split("-->")

def get_conn_connCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    # conn + connCtx
    if syntax_tree.tree == None:
        connCtx = "NONE_TREE"
    else:
        conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
        connCtx = get_node_Ctx(conn_node, syntax_tree)

    conn_connCtx = "%s|%s" % (conn_name, connCtx)

    return conn_connCtx

def get_conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        rightSiblingCtx = "NONE_TREE"
    else:
        rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        rightSiblingCtx = get_node_linked_Ctx(rightSibling_node, syntax_tree)

    conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

    return conn_rightSiblingCtx

def get_conn_leftSiblingCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        leftSiblingCtx = "NONE_TREE"
    else:
        leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        leftSiblingCtx = get_node_linked_Ctx(leftSibling_node, syntax_tree)

    conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

    return conn_leftSiblingCtx

def get_conn_parent_categoryCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = get_node_linked_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    return conn_parent_categoryCtx


