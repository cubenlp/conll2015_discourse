#coding:utf-8
from syntax_tree import Syntax_tree
from connective_dict import Connectives_dict
import util
from model_trainer.Non_Explicit_classifier.non_exp_dict_util import get_tense_in_sent
from nltk.stem.wordnet import WordNetLemmatizer

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

def get_self_category(syntax_tree, conn_indices):
    if syntax_tree.tree == None:
        self_category = "NONE_TREE"
    else:
        self_category = syntax_tree.get_self_category_node_by_token_indices(conn_indices).name
    return self_category

def get_parent_category(syntax_tree, conn_indices):
    if syntax_tree.tree == None:
        parent_category = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        if parent_category_node == None:
            parent_category = "ROOT"
        else:
            parent_category = parent_category_node.name
    return parent_category

def get_left_sibling_category(syntax_tree, conn_indices):
    if syntax_tree.tree == None:
        left_sibling_category = "NONE_TREE"
    else:
        left_sibling_category_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        if left_sibling_category_node == None:
            left_sibling_category = "NONE"
        else:
            left_sibling_category = left_sibling_category_node.name
    return left_sibling_category

def get_right_sibling_category(syntax_tree, conn_indices):
    if syntax_tree.tree == None:
        right_sibling_category = "NONE_TREE"
    else:
        right_sibling_category_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        if right_sibling_category_node == None:
            right_sibling_category = "NONE"
        else:
            right_sibling_category = right_sibling_category_node.name

    return right_sibling_category

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

def get_conn_next(parse_dict, DocID, sent_index, conn_indices):
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

    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    return "%s_%s" % (conn_name, next)

def get_conn_connCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree == None:
        connCtx = "NONE_TREE"
    else:
        conn_node = syntax_tree.get_self_category_node_by_token_indices(conn_indices)
        connCtx = get_node_Ctx(conn_node, syntax_tree)

    conn_connCtx = "%s|%s" % (conn_name, connCtx)

    return conn_connCtx

def get_conn_rightSiblingCtx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        rightSiblingCtx = "NONE_TREE"
    else:
        rightSibling_node = syntax_tree.get_right_sibling_category_node_by_token_indices(conn_indices)
        rightSiblingCtx = get_node_linked_Ctx(rightSibling_node, syntax_tree)

    conn_rightSiblingCtx = "%s|%s" % (conn_name, rightSiblingCtx)

    return conn_rightSiblingCtx

def get_conn_parent_category_Ctx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = get_node_linked_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    return conn_parent_categoryCtx

def get_conn_leftSibling_ctx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        leftSiblingCtx = "NONE_TREE"
    else:
        leftSibling_node = syntax_tree.get_left_sibling_category_node_by_token_indices(conn_indices)
        leftSiblingCtx = get_node_linked_Ctx(leftSibling_node, syntax_tree)

    conn_leftSiblingCtx = "%s|%s" % (conn_name, leftSiblingCtx)

    return conn_leftSiblingCtx

def get_CParent_to_root_path_node_names(parse_dict, DocID, sent_index, conn_indices):
    #获取该句话的语法树
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


def get_conn_parent_category_not_linked_Ctx(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        parent_categoryCtx = "NONE_TREE"
    else:
        parent_category_node = syntax_tree.get_parent_category_node_by_token_indices(conn_indices)
        parent_categoryCtx = get_node_Ctx(parent_category_node, syntax_tree)

    conn_parent_categoryCtx = "%s|%s" % (conn_name, parent_categoryCtx)

    return conn_parent_categoryCtx

def get_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    return get_prev_conn_curr_sentence(parse_dict, DocID, sent_index, conn_indices)

def get_prev_conn_curr_sentence(parse_dict, DocID, sent_index, conn_indices):

    prev_curr = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, conn_indices[0])]
    #prev_curr
    prev_curr_conns, _ = _check_connective_names(prev_curr)

    if prev_curr_conns != []:
        return prev_curr_conns[0]
    else:
        return "NULL"

def get_prev_conn_prev_sentence(parse_dict, DocID, sent_index, conn_indices):
    if sent_index > 0:
        prev_sent_tokens = [word[0] for word in parse_dict[DocID]["sentences"][sent_index - 1]["words"]]
        prev_sent_conns, _ = _check_connective_names(prev_sent_tokens)
        if prev_sent_conns != []:
            return prev_sent_conns[0]
        else:
            return "NULL"
    else:
        return "NULL"

def get_prev_conn_curr_prev_sentence(parse_dict, DocID, sent_index, conn_indices):
    prev_sent_tokens = []
    if sent_index > 0:
        prev_sent_tokens = [word[0] for word in parse_dict[DocID]["sentences"][sent_index - 1]["words"]]

    prev_curr = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, conn_indices[0])]

    #prev_curr
    prev_curr_conns, _ = _check_connective_names(prev_curr)
    prev_sent_conns, _ = _check_connective_names(prev_sent_tokens)

    if prev_curr_conns != []:
        return prev_curr_conns[0]
    else:
        if prev_sent_conns != []:
            return prev_sent_conns[0]
        else:
            return "NULL"



# def get_prev_connPOS(parse_dict, DocID, sent_index, conn_indices):
#     prev_sent_tokens = []
#     if sent_index > 0:
#         prev_sent_tokens = [word[0] for word in parse_dict[DocID]["sentences"][sent_index - 1]["words"]]
#
#     prev_curr = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, conn_indices[0])]
#
#     prev_tokens = prev_sent_tokens + prev_curr
#
#     _, prev_conn_indices = _check_connective_names(prev_tokens)
#
#     if prev_conn_indices == []:
#         return "NULL"
#     else:
#
#         return prev_conn_indices[0]

#前面一个连接词 和 他的 pos
def get_prev_conn_POS(parse_dict, DocID, sent_index, conn_indices):
    prev_conn = get_prev_conn(parse_dict, DocID, sent_index, conn_indices)



#连接词＋前一个连接词（只到前一句）
def get_conn_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    prev_conn = get_prev_conn(parse_dict, DocID, sent_index, conn_indices)

    return "%s|%s" % (prev_conn, conn_name)

#as＋前一个连接词（只到前一句）
def get_as_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "as":
        prev_conn = get_prev_conn_curr_sentence(parse_dict, DocID, sent_index, conn_indices)
        return prev_conn
    else:
        return "NOT_as"

def get_as_prev_connPOS(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "as":
        prev_curr = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, conn_indices[0])]
        #prev_curr
        _, indices = _check_connective_names(prev_curr)

        if indices!= []:
            connPOS = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"] for index in indices[0]])
            return connPOS
        else:
            return "NULL"
    else:
        return "NOT_as"

#when＋前一个连接词（只到当前), 如果是 "When" 考虑前面一句
def get_when_prev_conn(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "when":
        prev_conn = get_prev_conn_curr_sentence(parse_dict, DocID, sent_index, conn_indices)
        return "%s_%s" % (conn_name, prev_conn)
    else:
        return "NOT_when"

def get_when_prev_connPOS(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "when":
        prev_curr = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(0, conn_indices[0])]
        #prev_curr
        _, indices = _check_connective_names(prev_curr)

        if indices!= []:
            connPOS = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"] for index in indices[0]])
            return connPOS
        else:
            return "NULL"
    else:
        return "NOT_when"

# 句子中 as的前半句， as的后半句 的时态,只是小些的tense
# [("I", "PRP"), ("love", "VBP"), ("China", "NNP")]
def get_as_before_after_tense(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "as":
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

        as_before_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(0, conn_indices[0])
        ]
        as_after_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(conn_indices[-1] + 1, sent_length)
        ]

        as_before_tense = get_tense_in_sent(as_before_word_pos_list)
        as_after_tense = get_tense_in_sent(as_after_word_pos_list)
        as_before_tense = _get_coarse_tense(as_before_tense)
        as_after_tense = _get_coarse_tense(as_after_tense)

        return "%s|%s" % (as_before_tense, as_after_tense)

    else:
        return "NOT_as"

# 句子中 when的前半句， when的后半句 的时态,只是小些的tense
# [("I", "PRP"), ("love", "VBP"), ("China", "NNP")]
def get_when_before_after_tense(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "when":
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

        when_before_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(0, conn_indices[0])
        ]
        when_after_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(conn_indices[-1] + 1, sent_length)
        ]

        when_before_tense = get_tense_in_sent(when_before_word_pos_list)
        when_after_tense = get_tense_in_sent(when_after_word_pos_list)
        when_before_tense = _get_coarse_tense(when_before_tense)
        when_after_tense = _get_coarse_tense(when_after_tense)

        return "%s|%s" % (when_before_tense, when_after_tense)

    else:
        return "NOT_when"

def get_when_after_lemma_verbs(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "when":
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

        when_after_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(conn_indices[-1] + 1, sent_length)
        ]
        lemma_verbs = []
        lmtzr = WordNetLemmatizer()
        for word, pos in when_after_word_pos_list:
            if pos in ["VBD", "VBN", "VB", "VBP", "VBZ", "VBG"]:
                lemma_verbs.append(lmtzr.lemmatize(word, "v"))
        if lemma_verbs == []:
            return "NULL"
        else:
            return lemma_verbs[0]

    else:
        return "NOT_when"

# 句子中 as的前半句， as的后半句 的时态,只是小些的tense
# [("I", "PRP"), ("love", "VBP"), ("China", "NNP")]
def get_is_as_before_after_same_tense(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "as":
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

        as_before_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(0, conn_indices[0])
        ]
        as_after_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(conn_indices[-1] + 1, sent_length)
        ]

        as_before_tense = get_tense_in_sent(as_before_word_pos_list)
        as_after_tense = get_tense_in_sent(as_after_word_pos_list)

        # tense只分 past , present, future
        if _get_coarse_tense(as_before_tense) == _get_coarse_tense(as_after_tense):
            return "YES"
        else:
            return "NO"
    else:
        return "NOT_as"

# 在 when 中, 判断其前半句，后半句，中是否有表示状态的： he is at home when ...(同时发生）
def get_when_is_contain_status(parse_dict, DocID, sent_index, conn_indices):
    conn_name = get_C_String(parse_dict, DocID, sent_index, conn_indices)
    if conn_name == "when": # 前半句， 后半句
        sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

        when_before_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(0, conn_indices[0])
        ]
        # 前面到标点结束
        e = 0
        for index, (word, _) in enumerate(when_before_word_pos_list):
            if word in """!"#&'*+,-..../:;<=>?@[\]^_`|~""" + "``" + "''":
                e = index
        when_before_word_pos_list = when_before_word_pos_list[e:]

        when_after_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
                                    parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
                                   for index in range(conn_indices[-1] + 1, sent_length)
        ]
        if _is_contain_status(when_before_word_pos_list) or _is_contain_status(when_after_word_pos_list):
            # print " ".join([word for word, pos in when_before_word_pos_list]),
            # print "when " + " ".join([word for word, pos in when_after_word_pos_list])
            return "YES"
        else:
            return "NO"

    # elif conn_name == "When": #前一句，和 当前句
    #     curr_sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    #     curr_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index]["words"][index][0],
    #                             parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"])
    #                             for index in range(0, curr_sent_length)]
    #     if _is_contain_status(curr_word_pos_list):
    #         return "YES"
    #
    #     if sent_index - 1 >= 0:
    #         prev_sent_length = len(parse_dict[DocID]["sentences"][sent_index - 1]["words"])
    #         prev_word_pos_list = [(parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0],
    #                             parse_dict[DocID]["sentences"][sent_index- 1]["words"][index][1]["PartOfSpeech"])
    #                             for index in range(0, prev_sent_length)]
    #
    #         if _is_contain_status(prev_word_pos_list):
    #             return "YES"
    #
    #     return "NO"
    else:
        return "NOT_when"

#[("I", "PRP"), ("love", "VBP"), ("China", "NNP")]
def _is_contain_status(word_pos_list):
    T = False
    for index, (word, pos) in enumerate(word_pos_list):
        if word in ["is", "am", "are", "was", "were", "been", "'s", "'re", "'m"]:
            # 看下一个词是不是动词的过去式
            if index + 1 <= len(word_pos_list) - 1:
                if word_pos_list[index + 1][1] not in ["VBD", "VBN"]:
                    T = True

    return T

# tense只分 past , present, future
def _get_coarse_tense(tense):
    if "past" in tense:
        return "past"

    if "present" in tense:
        return "present"

    if "future" in tense:
        return "future"

    return "NULL"



''' 识别sentence中的连接词, 返回识别出来的连接词的name # ["but", "in particular"] '''
def _check_connective_names(sent_tokens):
    sent_tokens = [word.lower() for word in sent_tokens ]
    indices = []
    conn_names = []
    tagged = set([])#已经标记列表
    sortedConn = Connectives_dict().sorted_conns_list
    for conn in sortedConn:
        #判断连接词是否在句子中出现
        if '..' in conn:#对于这种类型的在sentence中只识别一次
            c1, c2 = conn.split('..')
            c1_indice = util.getSpanIndecesInSent(c1.split(), sent_tokens)#[[7]]
            c2_indice = util.getSpanIndecesInSent(c2.split(), sent_tokens)#[[10]]
            if c1_indice!= [] and c2_indice != []:#词在句子中
                if c1_indice[0][0] < c2_indice[0][0]:#c1,c2 的先后顺序也不能错
                    #识别到该连接词
                    temp = set([t for t in (c1_indice[0]+c2_indice[0]) ])
                    #判断连接词是否已经被识别过了，如 已经识别了 for example 就不用去识别for 了
                    if tagged & temp == set([]):#没有被识别过，加入indices，加入tagged
                        indices.append(c1_indice[0]+c2_indice[0])# [[7], [10]]
                        conn_names.append(conn)
                        tagged = tagged.union(temp)
        else:
            c_indice = util.getSpanIndecesInSent(conn.split(), sent_tokens)#[[2,6],[1,3],...]
            if c_indice !=[]:
                #检查c_indice中每一项，如果该项在tagged中存在，剔除该项
                tt = []
                for item in c_indice:
                    if set(item) & tagged == set([]):
                        tt.append(item)
                c_indice = tt

                if c_indice != []:
                    indices.extend([item for item in c_indice])#[([2,6], 'for instance'), ....]
                    tagged = tagged.union(set([r for t in c_indice for r in t]))
                    conn_names.append(conn)
    return conn_names , indices



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