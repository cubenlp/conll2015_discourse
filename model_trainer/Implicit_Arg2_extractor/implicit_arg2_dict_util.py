#coding:utf-8
import copy
from syntax_tree import Syntax_tree
from clause import Arg_Clauses
from nltk.stem.wordnet import WordNetLemmatizer
import util


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
