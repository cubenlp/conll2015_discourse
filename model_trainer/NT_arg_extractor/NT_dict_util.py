#coding:utf-8
from syntax_tree import Syntax_tree
from constituent import Constituent
import config
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper
import operator
import util
import copy



#constituent with label(arg1,arg2 or none), paper
def get_constituents_with_label(parse_dict, connective):
    DocID = connective.DocID
    sent_index = connective.sent_index
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        return []

    conn_indices = connective.token_indices
    constituent_nodes = []
    if len(conn_indices) == 1:# like and or so...
        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_indices[0]).up
    else:
        conn_node = syntax_tree.get_common_ancestor_by_token_indices(conn_indices)

        conn_leaves = set([syntax_tree.get_leaf_node_by_token_index(conn_index) for conn_index in conn_indices])

        children = conn_node.get_children()
        for child in children:
            leaves = set(child.get_leaves())
            if conn_leaves & leaves == set([]):
                constituent_nodes.append(child)

    curr = conn_node
    while not curr.is_root():
        constituent_nodes.extend(syntax_tree.get_siblings(curr))
        curr = curr.up


    Arg1_token_indices = connective.Arg1_token_indices
    Arg2_token_indices = connective.Arg2_token_indices
    Arg1_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in Arg1_token_indices])
    Arg2_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in Arg2_token_indices])

    constituents = []
    for node in constituent_nodes:
        cons = Constituent(syntax_tree, node)
        cons.connective = connective
        leaves = set(node.get_leaves())
        if leaves <= Arg1_leaves:
            cons.label = "Arg1"
        elif leaves <= Arg2_leaves:
            cons.label = "Arg2"
        else:
            cons.label = "NULL"
        constituents.append(cons)

    return constituents

#constituent with label(arg1,arg2 or none),
def get_constituents_with_label2(parse_dict, connective):
    DocID = connective.DocID
    sent_index = connective.sent_index
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        return []

    conn_indices = connective.token_indices
    constituent_nodes = []
    if len(conn_indices) == 1:# like and or so...
        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_indices[0]).up
    else:
        conn_node = syntax_tree.get_common_ancestor_by_token_indices(conn_indices)

        conn_leaves = set([syntax_tree.get_leaf_node_by_token_index(conn_index) for conn_index in conn_indices])

        children = conn_node.get_children()
        for child in children:
            leaves = set(child.get_leaves())
            if conn_leaves & leaves == set([]):
                constituent_nodes.append(child)

    curr = conn_node
    while not curr.is_root():
        constituent_nodes.extend(syntax_tree.get_siblings(curr))
        curr = curr.up


    Arg1_token_indices = connective.Arg1_token_indices
    Arg2_token_indices = connective.Arg2_token_indices
    Arg1_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in Arg1_token_indices])
    Arg2_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in Arg2_token_indices])

    constituents = []
    for node in constituent_nodes:
        cons = Constituent(syntax_tree, node)
        cons.connective = connective
        leaves = set(node.get_leaves())
        if leaves <= Arg1_leaves:
            cons.label = "Arg1"
        elif leaves <= Arg2_leaves:
            cons.label = "Arg2"
        else:
            cons.label = "NULL"
        constituents.append(cons)

    return constituents


def get_conn_node(syntax_tree, conn_indices):
    if len(conn_indices) == 1:
        conn_node = syntax_tree.get_leaf_node_by_token_index(conn_indices[0]).up
    else:
        conn_node = syntax_tree.get_common_ancestor_by_token_indices(conn_indices)
    return conn_node

def get_CON_Str(parse_dict, DocID, sent_index, conn_indices):
    # get the name of connective
    C_String = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return C_String

def get_CON_POS(parse_dict, DocID, sent_index, conn_indices):
    # get the name of connective
    POS = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][1]["PartOfSpeech"] \
                  for word_token in conn_indices ])
    return POS

def get_prev1(parse_dict, DocID, sent_index, conn_indices):
    flag = 0
    prev_index = conn_indices[0] - 1
    pre_sent_index = sent_index
    if prev_index < 0:
        pre_sent_index -= 1
        prev_index = -1
        if pre_sent_index < 0:
            flag = 1
    # the previous word of the connective
    if flag == 1:
        prev1 = "prev1_NONE"
    else:
        prev1 = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]

    return prev1

def get_CON_iLSib(syntax_tree, conn_node):
    return len(syntax_tree.get_left_siblings(conn_node))

def get_CON_iRSib(syntax_tree, conn_node):
    return len(syntax_tree.get_right_siblings(conn_node))

def get_NT_Ctx(constituent):
    Ctx = []
    #self
    Ctx.append(constituent.node.name)
    #parent
    if constituent.node.up == None:
        Ctx.append("NULL")
    else:
        Ctx.append(constituent.node.up.name)
    #left
    left_siblings = constituent.syntax_tree.get_left_siblings(constituent.node)
    if left_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(left_siblings[-1].name)
    #right
    right_siblings = constituent.syntax_tree.get_right_siblings(constituent.node)
    if right_siblings == []:
        Ctx.append("NULL")
    else:
        Ctx.append(right_siblings[0].name)

    return "-".join(Ctx)


def get_CON_NT_Path(conn_node, constituent):
    node = constituent.node
    return constituent.syntax_tree.get_node_to_node_path(conn_node, node)

def get_CON_NT_Position(conn_node, constituent):
    return constituent.syntax_tree.get_relative_position(conn_node, constituent.node)


def get_NT_prev_curr_Path(i, constituents):
    if i == 0:
        return "NONE"
    curr = constituents[i].node
    prev = constituents[i - 1].node
    return constituents[i].syntax_tree.get_node_to_node_path(curr, prev)

def get_NT_prev_curr_production_rule(i, constituents):
    if i == 0:
        return "NONE"
    curr = constituents[i].node
    prev = constituents[i - 1].node
    common_ancestor = constituents[i].syntax_tree.tree.get_common_ancestor([curr, prev])

    return common_ancestor.name


def has_SBAR_ancestor(constituent):
    T = False
    node = constituent.node
    if node.is_root():
        return T
    node = node.up
    while not node.is_root():
        if node.name == "SBAR":
            T = True
            break
        node = node.up
    return T


def get_sent_clauses(parse_dict, DocID, sent_index):


    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    sent_tokens = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, sent_length)]

    punctuation = "...,:;?!~--"
    # first, use punctuation symbols to split the sentence
    _clause_indices_list = []#[[(1,"I")..], ..]
    temp = []
    for index, word in sent_tokens:
        if word not in punctuation:
            temp.append((index, word))
        else:
            if temp != []:
                _clause_indices_list.append(temp)
                temp = []
    clause_indices_list = []
    for clause_indices in _clause_indices_list:
        temp = util.list_strip_punctuation(clause_indices)
        if temp != []:
            clause_indices_list.append([item[0] for item in temp])

    # then use SBAR tag in its parse tree to split each part into clauses.
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        return []

    clause_list = []
    for clause_indices in clause_indices_list:
        clause_tree = _get_subtree(syntax_tree, clause_indices)
        flag = 0
        for node in clause_tree.tree.traverse(strategy="levelorder"):
            if node.name == "SBAR":
                temp1 = [node.index for node in node.get_leaves()]
                temp2 = sorted(list(set(clause_indices) - set(temp1)))

                if temp2 == []:
                    clause_list.append(temp1)
                else:
                    if temp1[0] < temp2 [0]:
                        clause_list.append(temp1)
                        clause_list.append(temp2)
                    else:
                        clause_list.append(temp2)
                        clause_list.append(temp1)

                flag = 1
                break
        if flag == 0:
            clause_list.append(clause_indices)

    return clause_list


def _get_subtree(syntax_tree, clause_indices):
    copy_tree = copy.deepcopy(syntax_tree)

    for index, leaf in enumerate(copy_tree.tree.get_leaves()):
        leaf.add_feature("index",index)

    clause_nodes = []
    for index in clause_indices:
        node = copy_tree.get_leaf_node_by_token_index(index)
        clause_nodes.append(node)

    for node in copy_tree.tree.traverse(strategy="levelorder"):
        node_leaves = node.get_leaves()
        if set(node_leaves) & set(clause_nodes) == set([]):
            node.detach()
    return copy_tree


def get_NT_NTparent_Ctx(constituent):
    node = constituent.node
    if node.is_root():
        return "%s|%s" % (node.name, "NO_PARENT")

    parent_Ctx = get_node_linked_Ctx(node.up)

    return "%s|%s" % (node.name, parent_Ctx)


# get the linked context of the node
def get_node_linked_Ctx(node):
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

def get_conn_name(parse_dict, DocID, sent_index, conn_indices):
    ''' conn_name '''
    # get the name of connective
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name

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
        rightSiblingCtx = get_node_linked_Ctx(rightSibling_node)

    conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

    return conn_rightSiblingCtx

def get_conn_parent_categoryCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = get_node_linked_Ctx(parent_category_node)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    return conn_parent_categoryCtx

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

def get_NT_Linked_ctx(constituent):
    node = constituent.node

    return get_node_linked_Ctx(node)

def get_NT_to_root_path(constituent):
    node = constituent.node
    syntax_tree = constituent.syntax_tree

    return syntax_tree.get_node_path_to_root(node)

def get_NT_parent_linked_ctx(constituent):
    node = constituent.node
    node = node.up

    return get_node_linked_Ctx(node)



if __name__ =="__main__":
    pass