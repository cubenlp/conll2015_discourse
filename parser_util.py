#coding:utf-8
import util, config, os, json
from connective_dict import Connectives_dict
from example import Example
import model_trainer.mallet_util as mallet_util
from model_trainer.NT_arg_extractor.constituent import Constituent
from syntax_tree import Syntax_tree
from connective import Connective
from clause import Arg_Clauses
import copy
import sys

def get_all_connectives(documents):
    conns_list = [] #[(DocID, sent_index, conn_indices), ()..]
    for DocID in documents:
        doc = documents[DocID]
        list = _get_doc_conns(doc) #[(sent_index, conn_indices), ()..]
        for sent_index, conn_indices in list:
            conns_list.append((DocID, sent_index, conn_indices))
    return conns_list

def _get_doc_conns(document):
    list = [] #[(sent_index, conn_indices), ()..]
    for sent_index, sentence in enumerate(document["sentences"]):
        sent_words_list = [word[0] for word in sentence["words"]]
        for conn_indices in _check_connectives(sent_words_list): #[[2, 3], [0]]
            list.append((sent_index, conn_indices))
    return list

# identify connectives in sentence (sent_tokens)
# return indices: [[2, 3], [0]]
def _check_connectives(sent_tokens):
    sent_tokens = [word.lower() for word in sent_tokens ]
    indices = []
    tagged = set([])
    sortedConn = Connectives_dict().sorted_conns_list
    for conn in sortedConn:
        if '..' in conn:
            c1, c2 = conn.split('..')
            c1_indice = util.getSpanIndecesInSent(c1.split(), sent_tokens)#[[7]]
            c2_indice = util.getSpanIndecesInSent(c2.split(), sent_tokens)#[[10]]
            if c1_indice!= [] and c2_indice != []:
                if c1_indice[0][0] < c2_indice[0][0]:
                    temp = set([t for t in (c1_indice[0]+c2_indice[0]) ])
                    if tagged & temp == set([]):
                        indices.append(c1_indice[0]+c2_indice[0])# [[7], [10]]
                        tagged = tagged.union(temp)
        else:
            c_indice = util.getSpanIndecesInSent(conn.split(), sent_tokens)#[[2,6],[1,3],...]
            if c_indice !=[]:
                tt = []
                for item in c_indice:
                    if set(item) & tagged == set([]):
                        tt.append(item)
                c_indice = tt

                if c_indice != []:
                    indices.extend([item for item in c_indice])#[([2,6], 'for instance'), ....]
                    tagged = tagged.union(set([r for t in c_indice for r in t]))
    return indices

#[(DocID, sent_index, conn_indices), ()..]
def conn_clf_print_feature(parse_dict, conns_list, feature_function, to_file):

    print "\tExtract features: [..]",
    example_list = []
    for DocID, sent_index, conn_indices in conns_list:
        feature = feature_function(parse_dict, DocID, sent_index, conn_indices)
        example = Example("", feature)
        example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)
    print "\r\tExtract features: [OK]"

def conn_clf_read_model_output(conn_clf_model_output, conns_list):
    # ['yes', 'no'...]
    pred_list = mallet_util.get_mallet_predicted_list(conn_clf_model_output)
    disc_conns = []
    for pred, conn in zip(pred_list, conns_list):
        if pred == "1":
            disc_conns.append(conn)
    return disc_conns

def arg_position_print_feature(parse_dict, conns_list, feature_function, to_file):

    print "\tExtract features: [..]",
    example_list = []
    for DocID, sent_index, conn_indices in conns_list:
        feature = feature_function(parse_dict, DocID, sent_index, conn_indices)
        example = Example("", feature)
        example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)
    print "\r\tExtract features: [OK]"

def arg_position_read_model_output(arg_position_model_output, conns_list):
    SS_conns_list = []
    PS_conns_list = []
    # ['SS', 'PS'...]
    pred_list = mallet_util.get_mallet_predicted_list(arg_position_model_output)
    for pred, conn in zip(pred_list, conns_list):
        if config.LABEL_TO_ARG_POSITION[pred] == "SS":
            SS_conns_list.append(conn)
        if config.LABEL_TO_ARG_POSITION[pred] == "PS":
            PS_conns_list.append(conn)

    return SS_conns_list, PS_conns_list

#[5, 6]

def divide_SS_conns_list(SS_conns_list):
    SS_conns_parallel_list = []
    SS_conns_not_parallel_list = []
    for conn in SS_conns_list:
        DocID, sent_index, conn_indices = conn
        parallel = False
        if len(conn_indices) > 1:
            for i in range(len(conn_indices)):
                if i + 1 < len(conn_indices) and conn_indices[i+1] - conn_indices[i] > 1:
                    parallel = True
        if parallel:
            SS_conns_parallel_list.append(conn)
        else:
            SS_conns_not_parallel_list.append(conn)

    return SS_conns_parallel_list, SS_conns_not_parallel_list


def get_all_connectives_for_NT(parse_dict, conns_list):
    connectives = []
    for index, conn in enumerate(conns_list):
        # turn to connective object
        DocID, sent_index, conn_indices = conn
        conn_name = get_conn_name(parse_dict, DocID, sent_index, conn_indices)
        connective = Connective(DocID, sent_index, conn_indices, conn_name)
        connective.relation_ID = index
        connectives.append(connective)
    return connectives

def constituent_print_feature(parse_dict, connectives, feature_function, to_file):

    print "\tExtract features: [..]",

    example_list = []

    # total = float(len(connectives))
    for curr_index, connective in enumerate(connectives):
        # print "process: %.2f%%.\r" % ((curr_index + 1)/total*100),

        constituents = _get_constituents(parse_dict, connective)
        constituents = sorted(constituents, key=lambda constituent: constituent.indices[0])   # sort by age
        # extract features for each constituent
        for i, constituent in enumerate(constituents):
            feature = feature_function(parse_dict, constituent, i, constituents)
            example = Example("", feature)
            example.comment = "%s|%s" % (constituent.connective.relation_ID, " ".join([str(t) for t in constituent.get_indices()]))
            example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"


def constituent_read_model_output(
        constituent_feat_path, constituent_model_output, parse_dict, conns_list):

    feat_file = open(constituent_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(constituent_model_output)

    feature_list = [line.strip() for line in feat_file]

    # relation_dict[relation_ID] = {(['1', '2'],'Arg1')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        constituent_indices = comment.split("|")[1].strip().split(" ")
        if relation_ID not in relation_dict:
            relation_dict[relation_ID] = [(constituent_indices, predicted)]
        else:
            relation_dict[relation_ID].append((constituent_indices, predicted))
    # merge arg1(arg2) for each relation
    # relation_dict[relation_ID] = ([0,1],[2,3])
    for relation_ID in relation_dict.keys():
        list = relation_dict[relation_ID]
        Arg1_list = []
        Arg2_list = []
        for span, label in list:
            if label == "Arg1":
                Arg1_list.extend(span)
            if label == "Arg2":
                Arg2_list.extend(span)

        Arg1_list = sorted([int(item) for item in Arg1_list])
        Arg2_list = sorted([int(item) for item in Arg2_list])

        relation_dict[relation_ID] = (Arg1_list, Arg2_list)

    temp = []
    source = "SS"
    for i, conn in enumerate(conns_list):
        DocID, sent_index, conn_indices = conn

        Arg1_list, Arg2_list = relation_dict[i]

        Arg1_list = merge_NT_Arg(Arg1_list, parse_dict, DocID, sent_index)
        Arg2_list = merge_NT_Arg(Arg2_list, parse_dict, DocID, sent_index)

        if Arg1_list != [] and Arg2_list != []:
            temp.append((source, DocID, sent_index, conn_indices, Arg1_list, Arg2_list))
        else:
            pass
            # Arg1 or Arg2 is not identified
            # temp.append((source, DocID, sent_index, conn_indices, Arg1_list, Arg2_list))
            # if Arg1_list == []:
            #     print "Arg1###" + DocID, sent_index, conn_indices
            # if Arg2_list == []:
            #     print "Arg2###" + DocID, sent_index, conn_indices
            # if Arg1_list == [] and Arg2_list == []:
            #     print "Both###" + DocID, sent_index, conn_indices


    return temp

def merge_NT_Arg(Arg_list, parse_dict, DocID, sent_index):
    punctuation = """!"#&'*+,-..../:;<=>?@[\]^_`|~""" + "``" + "''"
    if len(Arg_list) <= 1:
        return Arg_list
    temp = []
    # scan the missing parts, if it is the punctuation, then make up
    for i, item in enumerate(Arg_list):
        if i <= len(Arg_list) - 2:
            temp.append(item)
            next_item = Arg_list[i + 1]
            if next_item - item > 1:
                flag = 1
                for j in range(item + 1, next_item):
                    if parse_dict[DocID]["sentences"][sent_index]["words"][j][0] not in punctuation:
                        flag = 0
                        break
                if flag == 1:# make up
                    temp += range(item + 1, next_item)
    temp.append(Arg_list[-1])

    Arg = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in temp]
    # remove the leading or tailing punctuations
    Arg = util.list_strip_punctuation(Arg)

    Arg = [item[0] for item in Arg]

    return Arg


def get_Args_for_SS_parallel_conns(parse_dict, SS_conns_parallel_list):
    temp = []
    source = "SS"
    for conn in SS_conns_parallel_list:
        DocID, sent_index, conn_indices = conn
        if len(conn_indices) == 2:# if then ,either or, neither nor
            conn_1_index = conn_indices[0]
            conn_2_index = conn_indices[1]

            Arg1 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) \
                        for index in range(conn_1_index+1, conn_2_index)]

            sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            Arg2 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) \
                        for index in range(conn_2_index+1, sent_length)]

            Arg1 = util.list_strip_punctuation(Arg1)
            Arg2 = util.list_strip_punctuation(Arg2)

            Arg1 = [item[0] for item in Arg1]
            Arg2 = [item[0] for item in Arg2]

            temp.append((source, DocID, sent_index, conn_indices, Arg1, Arg2))

        elif len(conn_indices) == 8:# on the one hand on the other hand
            conn_1_index = conn_indices[3]
            conn_2_index = conn_indices[7]

            Arg1 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) \
                        for index in range(conn_1_index+1, conn_2_index)]

            sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            Arg2 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) \
                        for index in range(conn_2_index+1, sent_length)]

            Arg1 = util.list_strip_punctuation(Arg1)
            Arg2 = util.list_strip_punctuation(Arg2)

            Arg1 = [item[0] for item in Arg1]
            Arg2 = [item[0] for item in Arg2]

            temp.append((source, DocID, sent_index, conn_indices, Arg1, Arg2))

    return temp

def get_Args_for_PS_conns(parse_dict, PS_conns_list):
    source = "PS"
    temp = []
    for conn in PS_conns_list:
        DocID, sent_index, conn_indices = conn

        if sent_index - 1 < 0:
            continue

        # the length of the previous sentence
        prev_length = len(parse_dict[DocID]["sentences"][sent_index - 1]["words"])
        Arg1 = [(index, parse_dict[DocID]["sentences"][sent_index - 1]["words"][index][0])
                for index in range(0, prev_length)]

        Arg1 = util.list_strip_punctuation(Arg1)

        # the length of the current sentence
        curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
        Arg2 = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, curr_length)]

        Arg2 = util.list_strip_punctuation(Arg2)

        Arg1 = [item[0] for item in Arg1]
        Arg2 = [item[0] for item in Arg2]

        temp.append((source, DocID, sent_index, conn_indices, Arg1, Arg2))

    return temp


def explicit_clf_print_feature(parse_dict, conns_list_args, feature_function, to_file):

    print "\tExtract features: [..]",

    example_list = []
    for conn in conns_list_args:
        source, DocID, sent_index, conn_indices, Arg1, Arg2 = conn
        connective = Connective(DocID, sent_index, conn_indices, "")
        feature = feature_function(parse_dict, connective)
        example = Example("", feature)
        example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"


def explicit_clf_read_model_output(explicit_model_output, conns_list_args):
    pred_list = mallet_util.get_mallet_predicted_list(explicit_model_output)
    pred_list = [config.Label_To_Sense[item] for item in pred_list]

    temp = []
    for pred, conn in zip(pred_list, conns_list_args):
        source, DocID, sent_index, conn_indices, Arg1, Arg2 = conn
        temp.append((source, DocID, sent_index, conn_indices, Arg1, Arg2, pred))
    return temp

def get_explicit_relations(parse_dict, conns_args_sense_list):
    SS_explicit_relations = []
    PS_explicit_relations = []
    for index, conn in enumerate(conns_args_sense_list):
        source, DocID, sent_index, conn_indices, Arg1, Arg2, sense = conn

        if source == "SS":
            conn_token_list = get_doc_offset(parse_dict, DocID, sent_index, conn_indices)
            Arg1_list = get_doc_offset(parse_dict, DocID, sent_index, Arg1)
            Arg2_list = get_doc_offset(parse_dict, DocID, sent_index, Arg2)

            # print Arg1
            # print Arg1_list
            relation = {}
            relation["ID"] = index
            relation['DocID'] = DocID
            relation['Arg1'] = {}
            relation['Arg1']['TokenList'] = Arg1_list
            relation['Arg2'] = {}
            relation['Arg2']['TokenList'] = Arg2_list
            relation['Type'] = 'Explicit'
            relation['Sense'] = [sense]
            relation['Connective'] = {}
            relation['Connective']['TokenList'] = conn_token_list
            #  add four attributes: Arg1_sent_index, Arg2_sent_index, conn_name, conn_sent_offset
            relation["Arg1_sent_index"] = sent_index
            relation["Arg2_sent_index"] = sent_index
            relation["conn_sent_offset"] = conn_indices
            relation["conn_name"] = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

            SS_explicit_relations.append(relation)
        if source == "PS":
            if sent_index - 1 < 0:
                continue

            conn_token_list = get_doc_offset(parse_dict, DocID, sent_index, conn_indices)
            Arg1_list = get_doc_offset(parse_dict, DocID, sent_index - 1, Arg1)
            Arg2_list = get_doc_offset(parse_dict, DocID, sent_index, Arg2)

            relation = {}
            relation["ID"] = index
            relation['DocID'] = DocID
            relation['Arg1'] = {}
            relation['Arg1']['TokenList'] = Arg1_list
            relation['Arg2'] = {}
            relation['Arg2']['TokenList'] = Arg2_list
            relation['Type'] = 'Explicit'
            relation['Sense'] = [sense]
            relation['Connective'] = {}
            relation['Connective']['TokenList'] = conn_token_list
            #  add four attributes: Arg1_sent_index, Arg2_sent_index, conn_name, conn_sent_offset
            relation["Arg1_sent_index"] = sent_index - 1
            relation["Arg2_sent_index"] = sent_index
            relation["conn_sent_offset"] = conn_indices
            relation["conn_name"] = get_conn_name(parse_dict, DocID, sent_index, conn_indices)

            PS_explicit_relations.append(relation)

    return SS_explicit_relations + PS_explicit_relations


def test_explicit_relations(explicit_relations):
    output = open(config.PARSER_EXPLICIT_REATION_PATH, 'w')
    for relation in explicit_relations:
        output.write('%s\n' % json.dumps(relation))
    output.close()

    print "-" * 120 + "\n Explicit Relation \n" + "-" * 120
    cmd = "python "+config.SCORER_PATH+" " \
          " "+config.JSON_GOLD_EXPLICIT_PATH+" "+config.PARSER_EXPLICIT_REATION_PATH+" "
    os.system(cmd)

def test_non_explicit_relations(non_explicit_relations):
    output = open(config.PARSER_NON_EXPLICIT_REATION_PATH, 'w')
    for relation in non_explicit_relations:
        output.write('%s\n' % json.dumps(relation))
    output.close()

    print "-" * 120 + "\n Non-Explicit Relation \n" + "-" * 120
    cmd = "python "+config.SCORER_PATH+" " \
          " "+config.JSON_GOLD_NON_EXPLICIT_PATH+" "+config.PARSER_NON_EXPLICIT_REATION_PATH+" "
    os.system(cmd)

def test_relation(relations):
    output = open(config.PARSER_REATION_PATH, 'w')
    for relation in relations:
        output.write('%s\n' % json.dumps(relation))
    output.close()

    print "-" * 120 + "\n All Relation \n" + "-" * 120
    cmd = "python "+config.SCORER_PATH+" " \
          " "+config.PDTB_ORIGIN_DEV_PATH+" "+config.PARSER_REATION_PATH+" "
    os.system(cmd)


def get_adjacent_non_exp_list(parse_dict, PS_conns_list):
    exp_rel_sent_pairs = {}# [DocID] = [(1,2),(8,9)...]
    for conn in PS_conns_list:
        DocID, sent_index, conn_indices = conn
        if sent_index == 0:
            continue
        if DocID not in exp_rel_sent_pairs:
            exp_rel_sent_pairs[DocID] = [(sent_index - 1, sent_index)]
        else:
            exp_rel_sent_pairs[DocID].append((sent_index - 1, sent_index))
    for DocID in exp_rel_sent_pairs:
        exp_rel_sent_pairs[DocID] = set(exp_rel_sent_pairs[DocID])

    #[(DocID,sent1_index,sent2_index) ]
    adjacent_non_exp_list = []
    for DocID in parse_dict:
        sent_count = len(parse_dict[DocID]["sentences"])
        adj_pair_set = _get_adj_pair_set(sent_count)
        adj_exp_pair_set = set([])
        if DocID in exp_rel_sent_pairs:
            adj_exp_pair_set = exp_rel_sent_pairs[DocID]

        adj_non_exp_pair_set = adj_pair_set - adj_exp_pair_set

        for sent1_index, sent2_index in adj_non_exp_pair_set:
            adjacent_non_exp_list.append((DocID, sent1_index, sent2_index))

    # remove inter-paragraph sentence pairs
    adjacent_non_exp_list = _remove_inter_paragraph_sent_pairs(parse_dict, adjacent_non_exp_list)


    return adjacent_non_exp_list

#[(DocID,sent1_index,sent2_index) ]
# remove inter-paragraph sentence pairs
def _remove_inter_paragraph_sent_pairs(parse_dict, adjacent_non_exp_list):
    temp = []
    for DocID, sent1_index, sent2_index in adjacent_non_exp_list:
        p1 = parse_dict[DocID]["sentences"][sent1_index]["paragraph"]
        p2 = parse_dict[DocID]["sentences"][sent2_index]["paragraph"]
        if p1 < 0 or p2 < 0:# can not get paragraph info
            temp.append((DocID, sent1_index, sent2_index))
            continue
        if p1 == p2:# in same paragraph
            temp.append((DocID, sent1_index, sent2_index))
    return temp

#[(DocID,sent1_index,sent2_index) ]
def get_non_explicit_relations(parse_dict, adjacent_non_exp_list):
    non_explicit_relations = []
    for index, (DocID, sent1_index, sent2_index) in enumerate(adjacent_non_exp_list):
        Arg1_offset_in_sent = _non_explicit_Arg_offset_in_sent(parse_dict, DocID, sent1_index)
        Arg2_offset_in_sent = _non_explicit_Arg_offset_in_sent(parse_dict, DocID, sent2_index)

        Arg1_TokenList = [ [-1, -1, -1, sent1_index, offset] for offset in Arg1_offset_in_sent]
        Arg2_TokenList = [ [-1, -1, -1, sent2_index, offset] for offset in Arg2_offset_in_sent]

        relation = {}
        relation["ID"] = index
        relation['DocID'] = DocID
        relation['Arg1'] = {}
        relation['Arg1']['TokenList'] = Arg1_TokenList
        relation['Arg2'] = {}
        relation['Arg2']['TokenList'] = Arg2_TokenList
        relation['Type'] = 'Implicit'
        relation['Connective'] = {}
        relation['Connective']['TokenList'] = []
        non_explicit_relations.append(relation)

    return non_explicit_relations

def _non_explicit_Arg_offset_in_sent(parse_dict, DocID, sent_index):
    curr_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    Arg = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0])
                for index in range(0, curr_length)]
    Arg = util.list_strip_punctuation(Arg)
    Arg = [item[0] for item in Arg]
    return Arg

def non_explicit_clf_print_feature(parse_dict, non_explicit_relations, feature_function, non_explicit_context_dict, prev_context_conn, to_file):

    print "\tExtract features: [..]",

    example_list = []
    for relation in non_explicit_relations:
        feature_1 = feature_function(relation, parse_dict)
        feature_2 = prev_context_conn(relation, parse_dict, non_explicit_context_dict)
        feature = util.mergeFeatures([feature_1, feature_2])
        example = Example("", feature)
        example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"


def non_explicit_read_model_output(non_explicit_model_output, parse_dict, non_explicit_relations):
    pred_list = mallet_util.get_mallet_predicted_list(non_explicit_model_output)
    pred_list = [config.Label_To_Sense[item] for item in pred_list]
    temp = []
    for sense, relation in zip(pred_list, non_explicit_relations):
        relation['Sense'] = [sense]
        temp.append(relation)
    return temp

def divide_non_explicit_relations(non_explicit_relations, parse_dict):
    EntRel_relations = []
    Implicit_AltLex_relations = []
    for relation in non_explicit_relations:
        if relation['Sense'][0] == "EntRel":#= "EntRel"
            DocID = relation["DocID"]
            Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
            Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]
            Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
            Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]
            Arg1_list = get_doc_offset(parse_dict, DocID, Arg1_sent_index, Arg1_offset_in_sent)
            Arg2_list = get_doc_offset(parse_dict, DocID, Arg2_sent_index, Arg2_offset_in_sent)
            relation['Arg1']['TokenList'] = Arg1_list
            relation['Arg2']['TokenList'] = Arg2_list

            EntRel_relations.append(relation)
        else:
            Implicit_AltLex_relations.append(relation)
    # print "EntRel_relations:" + str(len(EntRel_relations))
    # print "Implicit_AltLex_relations:" + str(len(Implicit_AltLex_relations))

    return EntRel_relations, Implicit_AltLex_relations

def attri_print_feature(parse_dict, relations, attribution_feat_func, to_file):
    example_list = []
    total = float(len(relations))
    for curr_index, relation in enumerate(relations):
        sys.stdout.flush()
        print "Extract Attribution Feature: %.2f%%.\r" % ((curr_index + 1)/total*100),
        for arg_clauses in _get_arg_clauses(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                feature = attribution_feat_func(arg_clauses, clause_index, parse_dict)
                #example
                example = Example("", feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))
                example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)
    print "Attribution Feature : Done!"

def attri_read_model_output(attribution_feat_path, attribution_model_output, parse_dict, non_explicit_relations):
    feat_file = open(attribution_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(attribution_model_output)

    implicit_relations = {}
    for relation in non_explicit_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
        Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
        sent1_index = Arg1_sent_indices[0]
        sent2_index = Arg2_sent_indices[0]

        Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
        Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in Arg1_offset_in_sent]
        Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in Arg2_offset_in_sent]


        Arg1 = util.list_strip_punctuation(Arg1)
        Arg2 = util.list_strip_punctuation(Arg2)

        implicit_relations[(relation_ID, "Arg1")] = Arg1
        implicit_relations[(relation_ID, "Arg2")] = Arg2


    feature_list = [line.strip() for line in feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    # remove the attribution part for each argument of the relation
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]
        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)

        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    temp = []
    for relation in non_explicit_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        if (relation_ID, "Arg1") not in relation_dict:
            print "11"
            Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
        else:
            Arg1_offset_in_sent = relation_dict[(relation_ID, "Arg1")]

        if (relation_ID, "Arg2") not in relation_dict:
            print "22"
            Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]
        else:
            Arg2_offset_in_sent = relation_dict[(relation_ID, "Arg2")]


        # Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]

        Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
        Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]


        Arg1_list = get_doc_offset(parse_dict, DocID, Arg1_sent_index, Arg1_offset_in_sent)
        Arg2_list = get_doc_offset(parse_dict, DocID, Arg2_sent_index, Arg2_offset_in_sent)

        relation['Arg1']['TokenList'] = Arg1_list
        relation['Arg2']['TokenList'] = Arg2_list

        curr_length_1 = len(parse_dict[DocID]["sentences"][Arg1_sent_index]["words"])
        Arg1_sent_text = [parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0] for index in range(0, curr_length_1)]
        Arg1_text = [parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0] for index in Arg1_offset_in_sent]


        # print DocID, Arg1_sent_index
        # print " ".join(Arg1_sent_text)
        # print " ".join(Arg1_text)

        temp.append(relation)

    return temp


def _get_arg_clauses(parse_dict, relation):
    return [_arg_clauses(parse_dict, relation, "Arg1"), _arg_clauses(parse_dict, relation, "Arg2")]

def _get_arg1_clauses(parse_dict, relation):
    return [_arg_clauses(parse_dict, relation, "Arg1")]

def _get_arg2_clauses(parse_dict, relation):
    return [_arg_clauses(parse_dict, relation, "Arg2")]

def _arg_clauses(parse_dict, relation, Arg):
    DocID = relation["DocID"]
    Arg_sent_indices = sorted([item[3] for item in relation[Arg]["TokenList"]])
    Arg_token_indices = sorted([item[4] for item in relation[Arg]["TokenList"]])

    if len(set(Arg_sent_indices)) != 1:
        return []
    relation_ID = relation["ID"]
    sent_index = Arg_sent_indices[0]

    sent_tokens = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in Arg_token_indices]

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
    if temp != []:
        _clause_indices_list.append(temp)

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
        # BFS，
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
    clauses = []# [([1,2,3],yes), ([4, 5],no), ]
    for clause_indices in clause_list:
        clauses.append((clause_indices, ""))


    # print DocID, sent_index
    # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in Arg_token_indices])
    # print clauses

    return Arg_Clauses(relation_ID, Arg, DocID, sent_index, clauses)

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



# [(0, 1), (1, 2), (2, 3), (3, 4)]
def _get_adj_pair_set(length):
    i = 0
    list = []
    while i < length -1:
        list.append((i, i+1))
        i += 1
    return set(list)

def get_doc_offset(parse_dict, DocID, sent_index, list):
    offset = 0
    for i in range(sent_index):
        offset += len(parse_dict[DocID]["sentences"][i]["words"])
    temp = []
    for item in list:
        temp.append(item + offset)
    return temp


def _get_constituents(parse_dict, connective):
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

    # obtain the Constituent object according to the node.
    constituents = []
    for node in constituent_nodes:
        cons = Constituent(syntax_tree, node)
        cons.connective = connective
        constituents.append(cons)
    return constituents


def get_conn_name(parse_dict, DocID, sent_index, conn_indices):
    # obtain the name of the connective
    conn_name = " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][word_token][0] \
                  for word_token in conn_indices ])
    return conn_name.lower()

import codecs

def add_paragraph_info_for_parse(parse_dict, raw_path):
    for DocID in parse_dict:
        try:
            raw_file = open("%s/%s" % (raw_path, DocID))
            # raw_file = codecs.open("%s/%s" % (raw_path, DocID), encoding="utf-8", errors="ignore")

            paragTexts = getParagTexts(raw_file)# ["IamaDoy","asas']
            for sent_index in range(len(parse_dict[DocID]["sentences"])):
                sent_words_list = [word[0] for word in parse_dict[DocID]["sentences"][sent_index]["words"]]
                ParagIndex = getParagIndex(paragTexts, sent_words_list)
                parse_dict[DocID]["sentences"][sent_index]["paragraph"] = ParagIndex

        except IOError:
            # if failed, set parse_dict[DocID]["sentences"][sent_index]["paragraph"] = -1
            for sent_index in range(len(parse_dict[DocID]["sentences"])):
                parse_dict[DocID]["sentences"][sent_index]["paragraph"] = -1







def add_paragraph_info(raw_file, doc):
    paragTexts = getParagTexts(raw_file)

    for sentence in doc["sentences"]:
        sent_words_list = [word[0] for word in sentence["words"]]
        ParagIndex = getParagIndex(paragTexts, sent_words_list)
        sentence["paragraph"] = ParagIndex
        # print sent_words_list
        # print ParagIndex
    pass

def getParagTexts(raw_file):
        text = [line.strip() for line in raw_file.readlines()]+['']
        t = 0
        for line in text:
            if line == '.START' or line == "":
                t += 1
            else:
                break
        text = text[t:]

        paragTexts =[]
        paragText = ""
        for line in text:
            if line != '':
                line = unicode(line, "utf-8", errors='ignore')
                paragText += line.replace(" ", "")
            else:
                if paragText != "":
                    paragText = util.removePuctuation(paragText)
                    paragTexts.append(paragText)
                    paragText = ""
        return paragTexts

def getParagIndex(paragTexts, sent_tokens):
    paragIndex = -1
    sent = "".join(sent_tokens)
    sent = sent.replace("-LCB-", "")
    sent = sent.replace("-LRB-", "")
    sent = sent.replace("-RCB-", "")
    sent = sent.replace("-RRB-", "")
    sent = util.removePuctuation(sent)


    matchedParag = set([])
    for index, paragText in enumerate(paragTexts):
        if sent in paragText:
            matchedParag.add(index)

    #matchedParag might be [1],[3,6] , take the minimum
    if matchedParag != set([]):
        paragIndex = min(matchedParag)
        # remove the sent which have been matched
        paragTexts[paragIndex] = paragTexts[paragIndex].replace(sent, "", 1)

    # if paragIndex == -1:
    #     print sent_tokens
    #     raise ValueError("sentence : '%s' , can not get the paragIndex" % (sent) )


    return paragIndex

def put_feature_to_model(feature_path, model_path, model_output_path):
    cmd = config.MALLET_PATH + "/bin/mallet classify-file --input " + feature_path + " --output " + model_output_path + " --classifier " + model_path
    os.system(cmd)


def _change_feature_dimension(test_file_path, n_features):
        file = open(test_file_path)
        lines = []
        flag = 0
        for line in file:# 175:1 21381:1 #
            line = line.rstrip()
            if flag == 0 and line.split("#")[0].strip() != "":
                last_feat_dimension = int(line.split("#")[0].rstrip().split(" ")[-1].split(":")[0])
                if last_feat_dimension < n_features:
                    line = line.split("#")[0] +"%d:0 #" % n_features + line.split("#")[1]
                    flag = 1

            line = "-1" + line
            lines.append(line)
        file.close()
        file = open(test_file_path, "w")
        file.write("\n".join(lines))
        file.close()


def ps_arg2_extractor_print_feature(parse_dict, PS_conns_list_args, PS_Arg2_feat_func, to_file):

    print "\tExtract features: [..]",

    PS_relations = get_PS_relations_by_PS_conns_list(PS_conns_list_args)
    example_list = []
    # total = float(len(PS_relations))
    for curr_index, relation in enumerate(PS_relations):
        # print "process: %.2f%%.\r" % ((curr_index + 1)/total*100),
        for arg_clauses in _get_ps_arg2_clauses(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                feature = PS_Arg2_feat_func(arg_clauses, clause_index, parse_dict)
                #example
                example = Example("", feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))

                example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"


def get_PS_relations_by_PS_conns_list(PS_conns_list_args):

    PS_relations = []

    for index, (source, DocID, sent_index, conn_indices, Arg1, Arg2) in enumerate(PS_conns_list_args):

        if sent_index - 1 < 0:
                continue

        Arg1_TokenList = [[-1, -1, -1, sent_index - 1, offset] for offset in Arg1]
        Arg2_TokenList = [[-1, -1, -1, sent_index, offset] for offset in Arg2]
        conn_token_list = [[-1, -1, -1, sent_index, offset] for offset in conn_indices]

        relation = {}
        relation["ID"] = "PS_%d" % index
        relation['DocID'] = DocID
        relation['Arg1'] = {}
        relation['Arg1']['TokenList'] = Arg1_TokenList
        relation['Arg2'] = {}
        relation['Arg2']['TokenList'] = Arg2_TokenList
        relation['Type'] = 'Explicit'
        relation['Sense'] = [""]
        relation['Connective'] = {}
        relation['Connective']['TokenList'] = conn_token_list
        #  add four attributes，Arg1_sent_index, Arg2_sent_index, conn_name, conn_sent_offset
        relation["Arg1_sent_index"] = sent_index - 1
        relation["Arg2_sent_index"] = sent_index
        relation["conn_sent_offset"] = conn_indices

        PS_relations.append(relation)

    return PS_relations



def _get_ps_arg2_clauses(parse_dict, relation):
    return [_ps_arg2_clauses(parse_dict, relation, "Arg2")]

def _ps_arg2_clauses(parse_dict, relation, Arg):
    DocID = relation["DocID"]
    relation_ID = relation["ID"]
    sent_index = relation[Arg]["TokenList"][0][3]
    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    sent_tokens = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, sent_length)]

    # first, split the sentence by the connective and the punctuation symbols
    conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
    punctuation = "...,:;?!~--"
    _clause_indices_list = []#[[(1,"I")..], ..]
    temp = []
    for index, word in sent_tokens:
        if word not in punctuation and index not in conn_token_indices:
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
        # BFS
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

    # print " ".join([parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)])
    # print clause_list
    # print Arg_list

    clauses = []# [([1,2,3],yes), ([4, 5],no), ]
    for clause_indices in clause_list:
        clauses.append((clause_indices, ""))

    gc = Arg_Clauses(relation_ID, Arg, DocID, sent_index, clauses)
    gc.conn_indices = conn_token_indices
    gc.conn_head_name = get_conn_name(parse_dict, DocID, sent_index, conn_token_indices)
    return gc


def ps_arg2_extractor_read_model_output(PS_Arg2_feat_path, PS_Arg2_model_output, parse_dict, PS_conns_list_args):

    PS_relations = get_PS_relations_by_PS_conns_list(PS_conns_list_args)

    feat_file = open(PS_Arg2_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(PS_Arg2_model_output)

    IPS_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    for relation in PS_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]
        sent2_index = relation["Arg2"]["TokenList"][0][3]
        curr_length_2 = len(parse_dict[DocID]["sentences"][sent2_index]["words"])

        Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in range(0, curr_length_2)]

        conn_indices = [item[4] for item in relation["Connective"]["TokenList"]]

        Arg2_part1 = Arg2[: conn_indices[0]]
        Arg2_part2 = Arg2[conn_indices[-1] + 1:]

        Arg2_part1 = util.list_strip_punctuation(Arg2_part1)
        Arg2_part2 = util.list_strip_punctuation(Arg2_part2)

        Arg2 = Arg2_part1 + Arg2_part2

        Arg2 = util.list_strip_punctuation(Arg2)

        IPS_relations[(relation_ID, "Arg2")] = Arg2

    feature_list = [line.strip() for line in feat_file]


    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = comment.split("|")[0].strip()
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    # remove the attribution part for each argument of the relation
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes": # need to remove
                implicit_Arg = IPS_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                IPS_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in IPS_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    temp = []
    for relation in PS_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]


        if (relation_ID, "Arg2") not in relation_dict:
            # 使用默认的
            Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]
        else:
            Arg2_offset_in_sent = relation_dict[(relation_ID, "Arg2")]

        # [("PS", DocID, sent_index, conn_indices, Arg1, Arg2)]
        conn_sent_index = relation["Arg2_sent_index"]
        conn_indices = relation["conn_sent_offset"]
        Arg1 = [item[4] for item in relation['Arg1']['TokenList']]
        Arg2 = Arg2_offset_in_sent

        T = ("PS", DocID, conn_sent_index, conn_indices, Arg1, Arg2)

        temp.append(T)

    return temp


def get_non_explicit_context_dict(explicit_relations):
    context_dict = {}
    for relation in explicit_relations:
        DocID = relation["DocID"]

        sent1_index = relation["Arg1_sent_index"]
        sent2_index = relation["Arg2_sent_index"]
        conn_indices = relation["conn_sent_offset"]
        conn_name = relation["conn_name"]
        conn_indices_string = " ".join([str(x) for x in conn_indices])
        sense = relation["Sense"][0]

        if (DocID, sent1_index, sent2_index) not in context_dict:
            context_dict[(DocID, sent1_index, sent2_index)] = []
        context_dict[(DocID, sent1_index, sent2_index)].append((conn_indices_string, conn_name, sense))

    return context_dict


def ps_arg1_extractor_print_feature(parse_dict, PS_conns_list_args, PS_Arg1_feat_func, to_file):
    print "\tExtract features: [..]",

    PS_relations = get_PS_relations_by_PS_conns_list(PS_conns_list_args)
    example_list = []
    # total = float(len(PS_relations))
    for curr_index, relation in enumerate(PS_relations):
        # print "process: %.2f%%.\r" % ((curr_index + 1)/total*100),
        for arg_clauses in _get_ps_arg1_clauses(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                feature = PS_Arg1_feat_func(arg_clauses, clause_index, parse_dict)
                #example
                example = Example("", feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))

                example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"

def _get_ps_arg1_clauses(parse_dict, relation):
    return [_ps_arg1_clauses(parse_dict, relation, "Arg1")]

def _ps_arg1_clauses(parse_dict, relation, Arg):
    DocID = relation["DocID"]
    Arg_sent_indices = sorted([item[3] for item in relation[Arg]["TokenList"]])
    if len(set(Arg_sent_indices)) != 1:
        return []
    relation_ID = relation["ID"]
    sent_index = Arg_sent_indices[0]
    Arg_list = sorted([item[4] for item in relation[Arg]["TokenList"]])

    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])

    # sent_indices = sorted(list(set(range(0, sent_length)) - set(conn_token_indices)))
    sent_tokens = [(index, parse_dict[DocID]["sentences"][sent_index]["words"][index][0]) for index in range(0, sent_length)]

    # first, use punctuation symbols to split the sentence
    punctuation = "...,:;?!~--"
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
        # 层次遍历，
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

    conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]

    clauses = []# [([1,2,3],yes), ([4, 5],no), ]
    for clause_indices in clause_list:
        clauses.append((clause_indices, ""))

    gc = Arg_Clauses(relation_ID, Arg, DocID, sent_index, clauses)
    gc.conn_indices = conn_token_indices
    gc.conn_head_name = get_conn_name(parse_dict, DocID, sent_index + 1, conn_token_indices) # conn 在下一个句子
    return gc


def ps_arg1_extractor_read_model_output(PS_Arg1_feat_path, PS_Arg1_model_output, parse_dict, PS_conns_list_args):

    PS_relations = get_PS_relations_by_PS_conns_list(PS_conns_list_args)

    feat_file = open(PS_Arg1_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(PS_Arg1_model_output)

    IPS_relations = {} # dict[(relation_ID,Arg)] = [(1,"I")..]
    for relation in PS_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]
        sent1_index = relation["Arg1"]["TokenList"][0][3]
        curr_length_1 = len(parse_dict[DocID]["sentences"][sent1_index]["words"])

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in range(0, curr_length_1)]
        Arg1 = util.list_strip_punctuation(Arg1)
        IPS_relations[(relation_ID, "Arg1")] = Arg1

    feature_list = [line.strip() for line in feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = comment.split("|")[0].strip()
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    # remove the attribution part for each argument of the relation
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]

        for span, label in list:
            if label == "yes": # need to remove
                implicit_Arg = IPS_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                IPS_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)


        arg_list = [item[0] for item in IPS_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    temp = []
    for relation in PS_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        if (relation_ID, "Arg1") not in relation_dict:
            Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
        else:
            Arg1_offset_in_sent = relation_dict[(relation_ID, "Arg1")]

        # [("PS", DocID, sent_index, conn_indices, Arg1, Arg2)]
        conn_sent_index = relation["Arg2_sent_index"]
        conn_indices = relation["conn_sent_offset"]
        Arg1 = Arg1_offset_in_sent
        Arg2 = [item[4] for item in relation['Arg2']['TokenList']]

        T = ("PS", DocID, conn_sent_index, conn_indices, Arg1, Arg2)

        temp.append(T)

    return temp

def implicit_arg1_print_feature(parse_dict, Implicit_AltLex_relations, implicit_arg1_feat_func, to_file):

    print "\tExtract features: [..]",

    example_list = []
    # total = float(len(Implicit_AltLex_relations))
    for curr_index, relation in enumerate(Implicit_AltLex_relations):
        sys.stdout.flush()
        # print "implicit_arg1 Feature: %.2f%%.\r" % ((curr_index + 1)/total*100),
        for arg_clauses in _get_arg1_clauses(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                feature = implicit_arg1_feat_func(arg_clauses, clause_index, parse_dict)
                #example
                example = Example("", feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))
                example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"



def implicit_arg1_read_model_output(implicit_arg1_feat_path, implicit_arg1_model_output, parse_dict, Implicit_AltLex_relations):
    feat_file = open(implicit_arg1_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(implicit_arg1_model_output)

    implicit_relations = {}
    for relation in Implicit_AltLex_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
        sent1_index = Arg1_sent_indices[0]

        Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]

        Arg1 = [(index, parse_dict[DocID]["sentences"][sent1_index]["words"][index][0]) for index in Arg1_offset_in_sent]

        Arg1 = util.list_strip_punctuation(Arg1)

        implicit_relations[(relation_ID, "Arg1")] = Arg1


    feature_list = [line.strip() for line in feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    # remove the attribution part for each argument of the relation
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]
        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)

        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    temp = []
    for relation in Implicit_AltLex_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        if (relation_ID, "Arg1") not in relation_dict:
            Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
            Arg1_sent_index = Arg1_sent_indices[0]
            Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
            Arg1 = [(index, parse_dict[DocID]["sentences"][Arg1_sent_index]["words"][index][0]) for index in Arg1_offset_in_sent]

            Arg1 = util.list_strip_punctuation(Arg1)
            Arg1_offset_in_sent = [item[0] for item in Arg1]
        else:
            Arg1_offset_in_sent = relation_dict[(relation_ID, "Arg1")]

        Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]

        Arg1_list = get_doc_offset(parse_dict, DocID, Arg1_sent_index, Arg1_offset_in_sent)

        # only deal with Arg1
        relation['Arg1']['TokenList'] = Arg1_list

        temp.append(relation)

    return temp


def implicit_arg2_print_feature(parse_dict, Implicit_AltLex_relations, implicit_arg2_feat_func, to_file):

    print "\tExtract features: [..]",

    example_list = []
    # total = float(len(Implicit_AltLex_relations))
    for curr_index, relation in enumerate(Implicit_AltLex_relations):
        sys.stdout.flush()
        # print "implicit_arg2 Feature: %.2f%%.\r" % ((curr_index + 1)/total*100),
        for arg_clauses in _get_arg2_clauses(parse_dict, relation):
            if arg_clauses == []: continue
            for clause_index in range(len(arg_clauses.clauses)):
                feature = implicit_arg2_feat_func(arg_clauses, clause_index, parse_dict)
                #example
                example = Example("", feature)
                example.comment = "%s|%s|%s" % \
                    (arg_clauses.relation_ID, arg_clauses.Arg, " ".join([str(i) for i in arg_clauses.clauses[clause_index][0]]))
                example_list.append(example)
    # write example_list to file
    util.write_example_list_to_file(example_list, to_file)

    print "\r\tExtract features: [OK]"



def implicit_arg2_read_model_output(implicit_arg2_feat_path, implicit_arg2_model_output, parse_dict, Implicit_AltLex_relations):
    feat_file = open(implicit_arg2_feat_path)
    pred_list = mallet_util.get_mallet_predicted_list(implicit_arg2_model_output)

    implicit_relations = {}
    for relation in Implicit_AltLex_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]
        # 一个句子长度的Arg1
        Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
        sent2_index = Arg2_sent_indices[0]

        Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]

        Arg2 = [(index, parse_dict[DocID]["sentences"][sent2_index]["words"][index][0]) for index in Arg2_offset_in_sent]

        Arg2 = util.list_strip_punctuation(Arg2)

        implicit_relations[(relation_ID, "Arg2")] = Arg2


    feature_list = [line.strip() for line in feat_file]
    # relation_dict[(relation_ID,Arg)] = {([1, 2],'yes')....}
    relation_dict = {}
    for feature_line, predicted in zip(feature_list, pred_list):
        comment = feature_line.split("#")[1].strip()
        relation_ID = int(comment.split("|")[0].strip())
        Arg = comment.split("|")[1].strip()
        attri_indices = [int(i) for i in comment.split("|")[2].strip().split(" ")]
        if (relation_ID, Arg) not in relation_dict:
            relation_dict[(relation_ID, Arg)] = [(attri_indices, predicted)]
        else:
            relation_dict[(relation_ID, Arg)].append((attri_indices, predicted))

    # remove the attribution part for each argument of the relation
    for (relation_ID, Arg) in relation_dict.keys():
        list = relation_dict[(relation_ID, Arg)]#[([1, 2],'yes')....]
        for span, label in list:
            if label == "yes":
                implicit_Arg = implicit_relations[(relation_ID, Arg)]#dict[(relation_ID,Arg)] = [(1,"I")..]
                part1 = []
                part2 = []
                flag = 0
                for index, word in implicit_Arg:
                    if flag == 0 and index not in span:
                        part1.append((index, word))
                    if index in span:
                        flag = 1
                    if flag == 1 and index not in span:
                        part2.append((index, word))

                implicit_relations[(relation_ID, Arg)] = util.list_strip_punctuation(part1) + util.list_strip_punctuation(part2)

        arg_list = [item[0] for item in implicit_relations[(relation_ID, Arg)]]
        if arg_list == []:
            if Arg == "Arg1":
                relation_dict[(relation_ID, Arg)] = list[-1][0]
            else:
                relation_dict[(relation_ID, Arg)] = list[0][0]
        else:
            relation_dict[(relation_ID, Arg)] = arg_list

    temp = []
    for relation in Implicit_AltLex_relations:
        relation_ID = relation["ID"]
        DocID = relation["DocID"]

        if (relation_ID, "Arg2") not in relation_dict:
            Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
            Arg2_sent_index = Arg2_sent_indices[0]
            Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]
            Arg2 = [(index, parse_dict[DocID]["sentences"][Arg2_sent_index]["words"][index][0]) for index in Arg2_offset_in_sent]

            Arg2 = util.list_strip_punctuation(Arg2)
            Arg2_offset_in_sent = [item[0] for item in Arg2]

        else:
            Arg2_offset_in_sent = relation_dict[(relation_ID, "Arg2")]

        Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]

        Arg2_list = get_doc_offset(parse_dict, DocID, Arg2_sent_index, Arg2_offset_in_sent)

        # only deal with Arg2
        relation['Arg2']['TokenList'] = Arg2_list


        temp.append(relation)

    return temp


def change_arg_doc_offset(relations, parse_dict):

    temp = []
    for relation in relations:
        DocID = relation["DocID"]
        Arg1_doc_offset = relation['Arg1']['TokenList']
        Arg2_doc_offset = relation['Arg2']['TokenList']

        # [(sent_index, sent_offset),...]
        Arg1_list = []
        for sent_index, sent_offset in get_sent_offset(parse_dict, DocID, Arg1_doc_offset):
            Arg1_list.append([-1, -1, -1, sent_index, sent_offset])
        Arg2_list = []
        for sent_index, sent_offset in get_sent_offset(parse_dict, DocID, Arg2_doc_offset):
            Arg2_list.append([-1, -1, -1, sent_index, sent_offset])

        relation['Arg1']['TokenList'] = Arg1_list
        relation['Arg2']['TokenList'] = Arg2_list

        temp.append(relation)

    return temp


# [(sent_index, sent_offset),...]
def get_sent_offset(parse_dict, DocID, doc_offset_list):

    sent_count = len(parse_dict[DocID]["sentences"])
    temp = []
    for doc_offset in doc_offset_list:
        T = 0
        sent_index = 0
        while T <= doc_offset and sent_index < sent_count:
            T += len(parse_dict[DocID]["sentences"][sent_index]["words"])
            sent_index += 1
        sent_index -= 1
        offset = 0
        for i in range(sent_index):
            offset += len(parse_dict[DocID]["sentences"][i]["words"])
        sent_offset = doc_offset - offset

        temp.append((sent_index, sent_offset))

    return temp



def change_arg_sent_offset(non_explicit_relations, parse_dict):
    temp = []
    for relation in non_explicit_relations:
        # change the tokenlist of argument
        DocID = relation["DocID"]
        Arg1_offset_in_sent = [item[4] for item in relation["Arg1"]["TokenList"]]
        Arg2_offset_in_sent = [item[4] for item in relation["Arg2"]["TokenList"]]
        Arg1_sent_index = relation["Arg1"]["TokenList"][0][3]
        Arg2_sent_index = relation["Arg2"]["TokenList"][0][3]
        Arg1_list = get_doc_offset(parse_dict, DocID, Arg1_sent_index, Arg1_offset_in_sent)
        Arg2_list = get_doc_offset(parse_dict, DocID, Arg2_sent_index, Arg2_offset_in_sent)
        relation['Arg1']['TokenList'] = Arg1_list
        relation['Arg2']['TokenList'] = Arg2_list

        temp.append(relation)

    return temp