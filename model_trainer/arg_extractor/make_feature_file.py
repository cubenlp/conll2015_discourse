#coding:utf-8
from util import mergeFeatures
from example import Example
from util import mergeFeatures, write_example_list_to_file ,write_shuffled_example_list_to_file
from syntax_tree  import Syntax_tree

def arg_extractor_make_feature_file(pdtb_parse, feature_function_list, to_file):

    print "为 argument extractor 抽取特征：%s ." % (" ".join([f.func_name for f in feature_function_list]))

    parse_dict = pdtb_parse.parse_dict

    subordinating_conns_SS = pdtb_parse.pdtb.subordinating_conns_SS
    coordinating_conns_SS = pdtb_parse.pdtb.coordinating_conns_SS
    adverbial_conns_SS = pdtb_parse.pdtb.adverbial_conns_SS

    conns_SS = subordinating_conns_SS \
               + coordinating_conns_SS \
               + adverbial_conns_SS

    example_list = []

    for connective in conns_SS:
        #获取该句话的语法树
        DocID = connective.DocID
        sent_index = connective.sent_index

        Arg1_token_indices = connective.Arg1_token_indices
        Arg2_token_indices = connective.Arg2_token_indices

        parse_tree = parse_dict[DocID]["sentences"][sent_index]["parsetree"].strip()
        syntax_tree = Syntax_tree(parse_tree)

        print Arg1_token_indices
        print Arg2_token_indices
        print parse_tree
        print DocID, sent_index

        if syntax_tree.tree != None:
            for node in syntax_tree.get_arg1_arg2_None_nodes_list(Arg1_token_indices, Arg2_token_indices):
                features = [feature_function(syntax_tree, connective, node, parse_dict) for feature_function in feature_function_list]
                #合并特征
                feature = mergeFeatures(features)
                #特征target
                target = node.label
                #example
                example = Example(target, feature)
                #加node标示
                example.comment = "%s|%s|%s|%s" % (connective.relation_ID, DocID, str(sent_index), " ".join([str(i) for i in syntax_tree.get_internal_node_location(node)]))

                example_list.append(example)


    #将example_list写入文件
    write_example_list_to_file(example_list, to_file)
    # write_shuffled_example_list_to_file(example_list, to_file)#打乱的。
    print "连接词特征已经写入文件：%s ." % (to_file)