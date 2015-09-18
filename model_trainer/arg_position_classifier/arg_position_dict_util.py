#coding:utf-8
from syntax_tree import Syntax_tree
import util

def get_C_String(parse_dict ,DocID, sent_index, conn_indices):
    #获取连接词到名称
    C_String = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return C_String

def get_CPOS(parse_dict ,DocID, sent_index, conn_indices):
    pos_tag_list = []
    for conn_index in conn_indices:
        pos_tag_list.append(parse_dict[DocID]["sentences"][sent_index]["words"][conn_index][1]["PartOfSpeech"])
    pos_tag = "_".join(pos_tag_list)

    return pos_tag

def get_prev1(parse_dict, DocID, sent_index, conn_indices):
    flag = 0
    prev_index = conn_indices[0] - 1
    pre_sent_index = sent_index
    if prev_index < 0:
        pre_sent_index -= 1
        prev_index = -1
        if pre_sent_index < 0:
            flag = 1
    # 连接词的前面一个词
    if flag == 1:
        prev1 = "prev1_NONE"
    else:
        prev1 = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]

    return prev1

def get_prev1POS(parse_dict, DocID, sent_index, conn_indices):
    flag = 0
    prev_index = conn_indices[0] - 1
    pre_sent_index = sent_index
    if prev_index < 0:
        pre_sent_index -= 1
        prev_index = -1
        if pre_sent_index < 0:
            flag = 1
    # 连接词的前面一个词
    if flag == 1:
        prev1 = "prev1_NONE"
    else:
        prev1 = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][0]
    if prev1 == "prev1_NONE":
        prev1_pos = "prev1POS_NONE"
    else:
        prev1_pos = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev_index][1]["PartOfSpeech"]

    return prev1_pos

def get_prev2(parse_dict, DocID, sent_index, conn_indices):
    flag = 0
    prev2_index = conn_indices[0] - 2
    pre_sent_index = sent_index
    if prev2_index == -1:
        pre_sent_index -= 1
        if pre_sent_index < 0:
            flag = 1
    elif prev2_index == -2:
        pre_sent_index -= 1
        if pre_sent_index < 0:
            flag = 1
        elif len(parse_dict[DocID]["sentences"][pre_sent_index]["words"]) == 1:
            pre_sent_index -= 1
            if pre_sent_index < 0:
                flag = 1
            else:
                prev2_index = -1
    if flag == 1:
        prev2 = "prev2_NONE"
    else:
        prev2 = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev2_index][0]

    return prev2

def get_prev2POS(parse_dict, DocID, sent_index, conn_indices):
    flag = 0
    prev2_index = conn_indices[0] - 2
    pre_sent_index = sent_index
    if prev2_index == -1:
        pre_sent_index -= 1
        if pre_sent_index < 0:
            flag = 1
    elif prev2_index == -2:
        pre_sent_index -= 1
        if pre_sent_index < 0:
            flag = 1
        elif len(parse_dict[DocID]["sentences"][pre_sent_index]["words"]) == 1:
            pre_sent_index -= 1
            if pre_sent_index < 0:
                flag = 1
            else:
                prev2_index = -1
    if flag == 1:
        prev2 = "prev2_NONE"
    else:
        prev2 = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev2_index][0]

    if prev2 == "prev2_NONE":
        prev2_pos = "prev2POS_NONE"
    else:
        prev2_pos = parse_dict[DocID]["sentences"][pre_sent_index]["words"][prev2_index][1]["PartOfSpeech"]

    return prev2_pos


def get_next1_next1POS(parse_dict, DocID, sent_index, conn_indices):
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


    return next, nextPOS


def get_next2_next2POS(parse_dict, DocID, sent_index, conn_indices):
    #获取该句子长度，该doc的总句子数
    sent_count = len(parse_dict[DocID]["sentences"])
    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

    flag = 0
    next2_index = conn_indices[-1] + 2
    next2_sent_index = sent_index
    if conn_indices[-1] == sent_length - 2:
        next2_sent_index += 1
        next2_index = 0
        if next2_sent_index >= sent_count:
            flag = 1
    elif conn_indices[-1] == sent_length - 1:
        next2_sent_index += 1
        next2_index = 1
        if next2_sent_index >= sent_count:
            flag = 1
        elif len(parse_dict[DocID]["sentences"][next2_sent_index]["words"]) == 1:
            next2_sent_index += 1
            next2_index = 0
            if next2_sent_index >= sent_count:
                flag = 1
    # 连接词的后面第二个词
    if flag == 1:
        next2 = "NONE"
    else:
        next2 = parse_dict[DocID]["sentences"][next2_sent_index]["words"][next2_index][0]

    ''' next pos '''
    if next2 == "NONE":
        next2POS = "NONE"
    else:
        next2POS = parse_dict[DocID]["sentences"][next2_sent_index]["words"][next2_index][1]["PartOfSpeech"]


    return next2, next2POS

def get_conn_to_root_path(parse_dict, DocID, sent_index, conn_indices):
    #获取该句话的语法树
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        path = "NONE_TREE"
    else:
        path = ""
        for conn_index in conn_indices:
            conn_node = syntax_tree.get_leaf_node_by_token_index(conn_index)
            t = syntax_tree.get_node_path_to_root(conn_node)
            path += t + "&"
        if path[-1] == "&":
            path = path[:-1]

    return path