#coding:utf-8
from syntax_tree import Syntax_tree

def get_C_String(parse_dict ,DocID, sent_index, conn_indices):
    #获取连接词到名称
    C_String = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return C_String

def get_C_left_sibling_number(syntax_tree, conn_indices):
    C_Node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
    if C_Node.up == None:
        return 0
    children = C_Node.up.get_children()
    for i, child in enumerate(children):
        if id(C_Node) == id(child):
            return i

def get_C_right_sibling_number(syntax_tree, conn_indices):
    C_Node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
    if C_Node.up == None:
        return 0
    children = C_Node.up.get_children()
    for i, child in enumerate(children):
        if id(C_Node) == id(child):
            return len(children) - i - 1

def get_CParent_to_Node_path(syntax_tree, conn_indices, node):
    CParent = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
    common_ancestor = syntax_tree.tree.get_common_ancestor([CParent, node])

    path = ""
    # CParent->common_ancestor
    temp = CParent
    while temp != common_ancestor:
        path += temp.name +">"
        temp = temp.up
    path += common_ancestor.name
    ## common_ancestor -> node
    p =""
    temp = node
    while temp != common_ancestor:
        p = "<" + temp.name +p
        temp = temp.up
    path += p

    return path

def get_CParent_to_Node_path_length(syntax_tree, conn_indices, node):
    CParent = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
    common_ancestor = syntax_tree.tree.get_common_ancestor([CParent, node])

    length = 0
    # CParent->common_ancestor
    temp = CParent
    while temp != common_ancestor:
        temp = temp.up
        length += 1
    ## common_ancestor -> node
    temp = node
    while temp != common_ancestor:
        temp = temp.up
        length += 1

    return length


def get_relative_position_Node_to_C(syntax_tree, conn_indices, node):
    C_Node = syntax_tree.get_leaf_node_by_token_index(conn_indices[0])

    return syntax_tree.get_relative_position(C_Node, node)


# def get_relative_position_Node_to_C(syntax_tree, conn_indices, node):
#     C_Node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
#     common_ancestor = syntax_tree.tree.get_common_ancestor([C_Node, node])
#
#     position = ""
#     if common_ancestor == node:
#         position = "middle"
#     else:
#         #各自一直往左走，走到叶子节点
#
#         leaves = syntax_tree.tree.get_leaves()
#
#         C_t = C_Node
#         while not C_t.is_leaf():
#             C_t = C_t.get_children()[0]
#         node_t = node
#         while not node_t.is_leaf():
#             node_t = node_t.get_children()[0]
#
#         C_index = leaves.index(C_t)
#         node_index = leaves.index(node_t)
#
#         if node_index > C_index:
#             position = "right"
#         else:
#             position = "left"
#
#     return position










