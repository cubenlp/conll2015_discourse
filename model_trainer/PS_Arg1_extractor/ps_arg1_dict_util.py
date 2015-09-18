#coding:utf-8
import copy
from syntax_tree import Syntax_tree
from clause import Arg_Clauses
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import util
from connective_dict import Connectives_dict
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper


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

def get_curr_lowercased_verbs(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)

    verbs = []
    for index in curr_clause[0]:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            verbs.append(word.lower())

    return verbs


def get_curr_lemma_verbs(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)

    lmtzr = WordNetLemmatizer()

    verbs = []
    for index in curr_clause[0]:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            word = lmtzr.lemmatize(word, "v")
            verbs.append(word)

    return verbs


def get_curr_first(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    curr_first_index = curr_clause[0][0]
    curr_first = parse_dict[DocID]["sentences"][sent_index]["words"][curr_first_index][0]

    return curr_first

def get_curr_last(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    curr_last_index = curr_clause[0][-1]
    curr_last = parse_dict[DocID]["sentences"][sent_index]["words"][curr_last_index][0]

    return curr_last

def get_prev_last(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    prev_last_index = curr_clause[0][0] - 1
    if prev_last_index < 0:
        return "NONE"
    punctuation = "...,:;``''?--!~"
    prev_last_word = parse_dict[DocID]["sentences"][sent_index]["words"][prev_last_index][0]
    if prev_last_word not in punctuation:
        return prev_last_word
    else:
        temp = []
        index = prev_last_index
        while index >= 0:
            word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
            if word in punctuation:
                temp.append(word)
                index -= 1
            else:
                break
        return " ".join(temp)


def get_next_first(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    next_first_index = curr_clause[0][-1] + 1

    if next_first_index >= len(parse_dict[DocID]["sentences"][sent_index]["words"]):
        return "NONE"

    punctuation = "...,:;``''?--!~"
    next_first_word = parse_dict[DocID]["sentences"][sent_index]["words"][next_first_index][0]
    if next_first_word not in punctuation:
        return next_first_word
    else:
        temp = []
        index = next_first_index
        while index < len(parse_dict[DocID]["sentences"][sent_index]["words"]):
            word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
            if word in punctuation:
                temp.append(word)
                index += 1
            else:
                break
        return " ".join(temp)

def get_prev_last_curr_first(arg_clauses, clause_index, parse_dict):
    prev_last = get_prev_last(arg_clauses, clause_index, parse_dict)
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    prev_last_curr_first = "%s_%s" % (prev_last, curr_first)

    return prev_last_curr_first

def get_curr_last_next_first(arg_clauses, clause_index, parse_dict):
    curr_last = get_curr_last(arg_clauses, clause_index, parse_dict)
    next_first = get_next_first(arg_clauses, clause_index, parse_dict)
    curr_last_next_first = "%s_%s" % (curr_last, next_first)

    return curr_last_next_first


def get_curr_production_rule(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    subtrees = []
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree != None:
        clause_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in curr_clause_indices])
        no_need = []
        for node in syntax_tree.tree.traverse(strategy="levelorder"):
            if node not in no_need:
                if set(node.get_leaves()) <= clause_leaves:
                    subtrees.append(node)
                    no_need.extend(node.get_descendants())

    production_rule = []
    for tree in subtrees:
        for node in tree.traverse(strategy="levelorder"):
            if not node.is_leaf():
                rule = node.name + "-->" + " ".join([child.name for child in node.get_children()])
                production_rule.append(rule)

    return production_rule


def get_curr_position(arg_clauses, clause_index, parse_dict):
    length = len(arg_clauses.clauses)
    if length == 1:
        return "middle"
    elif length < 5:
        if clause_index == 0:
            return "left"
        elif clause_index == length - 1:
            return "right"
        else:
            return "middle"
    else:
        if clause_index <= 1:
            return "left"
        elif clause_index >= length - 2:
            return "right"
        else:
            return "middle"


def get_is_curr_NNP_prev_PRP_or_NNP(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NONE"
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    prev_clause_indices = arg_clauses.clauses[clause_index-1][0]

    curr_poses = set([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
                    for index in curr_clause_indices])

    prev_poses = set([parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
                    for index in prev_clause_indices])

    if set(["WHNP", "NNP"]) & curr_poses and set(["NNP", "PRP"]) & prev_poses != set([]):
        return "yes"
    else:
        return "no"


def get_prev_curr_production_rule(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    if clause_index > 0:
        prev_clause_index = clause_index - 1
        curr_clause_indices = arg_clauses.clauses[prev_clause_index][0] + curr_clause_indices

    subtrees = []
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)
    if syntax_tree.tree != None:
        clause_leaves = set([syntax_tree.get_leaf_node_by_token_index(index) for index in curr_clause_indices])
        no_need = []
        for node in syntax_tree.tree.traverse(strategy="levelorder"):
            if node not in no_need:
                if set(node.get_leaves()) <= clause_leaves:
                    subtrees.append(node)
                    no_need.extend(node.get_descendants())

    production_rule = []
    for tree in subtrees:
        for node in tree.traverse(strategy="levelorder"):
            if not node.is_leaf():
                rule = node.name + "-->" + " ".join([child.name for child in node.get_children()])
                production_rule.append(rule)

    return production_rule


def get_prev_curr_CP_production_rule(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return ["%s|%s" % ("NULL", rule) for rule in get_curr_production_rule(arg_clauses, clause_index, parse_dict)]

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    prev_production_rule = get_curr_production_rule(arg_clauses, clause_index - 1, parse_dict)

    CP_production_rule = []
    for curr_rule in curr_production_rule:
        for prev_rule in prev_production_rule:
            CP_production_rule.append("%s|%s" % (prev_rule, curr_rule))

    return CP_production_rule

def get_curr_next_CP_production_rule(arg_clauses, clause_index, parse_dict):
    if clause_index == len(arg_clauses.clauses) - 1:
        return ["%s|%s" % (rule, "NULL") for rule in get_curr_production_rule(arg_clauses, clause_index, parse_dict)]

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    next_production_rule = get_curr_production_rule(arg_clauses, clause_index + 1, parse_dict)

    CP_production_rule = []
    for curr_rule in curr_production_rule:
        for next_rule in next_production_rule:
            CP_production_rule.append("%s|%s" % (curr_rule, next_rule))

    return CP_production_rule

# prev: NP->NNP, curr: WHNP->WP
def get_is_NNP_WP(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NONE"

    curr_production_rule = get_curr_production_rule(arg_clauses, clause_index, parse_dict)
    prev_production_rule = get_curr_production_rule(arg_clauses, clause_index - 1, parse_dict)

    flag = 0
    for rule in curr_production_rule:
        part1, part2 = rule.split("-->")
        if "WHNP" in part1 and "WP" in part2:
            flag = 1
            break
    if flag == 1:
        for rule in prev_production_rule:
            part1, part2 = rule.split("-->")
            if "NP" in part1 and "NNP" in part2:
                return "yes"
        return "no"
    else:
        return "no"

#lemma verb ＋ prev 2 pos
def get_2prev_pos_lemma_verb(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    verb_pos = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    lmtzr = WordNetLemmatizer()

    first_verb = ""
    first_verb_index = 0
    for index in curr_clause_indices:
        word = parse_dict[DocID]["sentences"][sent_index]["words"][index][0]
        pos = parse_dict[DocID]["sentences"][sent_index]["words"][index][1]["PartOfSpeech"]
        if pos in verb_pos:
            word = lmtzr.lemmatize(word)
            first_verb = (word, index)
            break
        first_verb_index += 1
    if first_verb == "":
        return "NULL|NULL|NULL"
    if first_verb_index == 0:
        return "%s|%s|%s" % ("NULL", "NULL", first_verb[0])
    if first_verb_index == 1:
        prev1_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 1][1]["PartOfSpeech"]
        return "%s|%s|%s" % ("NULL", prev1_pos, first_verb[0])

    prev1_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 1][1]["PartOfSpeech"]
    prev2_pos = parse_dict[DocID]["sentences"][sent_index]["words"][first_verb[1] - 2][1]["PartOfSpeech"]
    return "%s|%s|%s" % (prev2_pos, prev1_pos, first_verb[0])

def get_curr_first_to_prev_last_path(arg_clauses, clause_index, parse_dict):
    if clause_index == 0:
        return "NULL"

    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    if syntax_tree.tree == None:
        return "NOTREE"

    curr_first_index = arg_clauses.clauses[clause_index][0][0]
    prev_last_index = arg_clauses.clauses[clause_index - 1][0][-1]

    curr_first_node = syntax_tree.get_leaf_node_by_token_index(curr_first_index).up
    prev_last_node = syntax_tree.get_leaf_node_by_token_index(prev_last_index).up

    path = syntax_tree.get_node_to_node_path(curr_first_node, prev_last_node)

    return path

# con str
def get_con_str(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name

# con str
def get_con_lstr(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name.lower()

# conn cate
def get_con_cat(arg_clauses, clause_index, parse_dict):
    conn_category = Connectives_dict().conn_category
    return conn_category[arg_clauses.conn_head_name]

def get_clause_conn_position(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices#[5]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)
    if conn_indices[0] > curr_clause_indices[-1]:
        return "left"
    else:
        return "right"

def get_clause_conn_distance(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices#[5]
    curr_clause_indices = arg_clauses.clauses[clause_index][0]# ([1,2,3],yes)

    if conn_indices[-1] < curr_clause_indices[0]:
        s = conn_indices[-1]
        e = curr_clause_indices[0]
    else:
        s = curr_clause_indices[-1]
        e = conn_indices[0]
    count = 0
    for clause_indices, _ in arg_clauses.clauses:
        if clause_indices[0] > s and clause_indices[-1] < e:
            count += 1
    return count

def get_conn_position_distance(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)
    position = get_clause_conn_position(arg_clauses, clause_index, parse_dict)
    distance = get_clause_conn_distance(arg_clauses, clause_index, parse_dict)

    return "%s_%s_%d" % (conn, position, distance)

# conn cate
def get_conn_to_root_path(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1
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

def get_conn_to_root_compressed_path(arg_clauses, clause_index, parse_dict):
    conn_indices = arg_clauses.conn_indices
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index + 1
    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

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

def get_conn_position(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)
    position = get_clause_conn_position(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, position)

def get_conn_curr_position(arg_clauses, clause_index, parse_dict):
    conn = get_con_str(arg_clauses, clause_index, parse_dict)

    curr_position = get_curr_position(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, curr_position)

# whether current clause contains "which"
def get_is_clause_contain_comma_which(arg_clauses, clause_index, parse_dict):
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index
    curr_clause = arg_clauses.clauses[clause_index]# ([1,2,3],yes)
    prev_last_index = curr_clause[0][0] - 1
    if prev_last_index < 0:
        return "NO"
    prev_last_word = parse_dict[DocID]["sentences"][sent_index]["words"][prev_last_index][0]

    prev_last_curr_first = "%s %s" % (prev_last_word, curr_first)

    if prev_last_curr_first == ", which":
        # print 1
        return "YES"
    else:
        # print 0
        return "NO"

def get_curr_first_prev_last_parse_path(arg_clauses, clause_index, parse_dict):
    DocID = arg_clauses.DocID
    sent_index = arg_clauses.sent_index

    if clause_index - 1 < 0:
        return "NONE"

    parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
    syntax_tree = Syntax_tree(parse_tree)

    curr_first_index = arg_clauses.clauses[clause_index][0][0]
    prev_last_index = arg_clauses.clauses[clause_index - 1][0][-1]

    curr_first_node = syntax_tree.get_leaf_node_by_token_index(curr_first_index)
    prev_last_node = syntax_tree.get_leaf_node_by_token_index(prev_last_index)

    path = syntax_tree.get_node_to_node_path(curr_first_node, prev_last_node)

    if path.find("<") != -1:
        path_1 = path[:path.find("<")]
        path_2 = path[path.find("<"):]
        return util.get_compressed_path_tag(path_1, ">") + util.get_compressed_path_tag(path_2, "<")
    else:
        return util.get_compressed_path_tag(path, ">")


def get_conn_curr_first(arg_clauses, clause_index, parse_dict):
    curr_first = get_curr_first(arg_clauses, clause_index, parse_dict)
    conn = get_con_lstr(arg_clauses, clause_index, parse_dict)

    return "%s_%s" % (conn, curr_first)



if __name__ == "__main__":
    pass