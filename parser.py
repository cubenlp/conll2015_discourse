#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("./")
import json
import parser_util
import config

from model_trainer.connective_classifier.feature_functions \
    import all_features as _conn_clf_feature_function

from model_trainer.arg_position_classifier.feature_functions\
    import all_features as _arg_position_feature_function

from model_trainer.NT_arg_extractor.feature_functions \
    import all_features as _constituent_feat_func

from model_trainer.Explicit_classifier.feature_functions \
    import all_features as _explicit_feat_func

from model_trainer.Non_Explicit_classifier.feature_functions \
    import all_features as _non_explicit_feat_func, prev_context_conn


from model_trainer.PS_Arg2_extractor.feature_functions \
    import all_features as _ps_arg2_extractor_feat_func

from model_trainer.PS_Arg1_extractor.feature_functions \
    import all_features as _ps_arg1_extractor_feat_func

from model_trainer.Implicit_Arg1_extractor.feature_functions \
    import all_features as _implicit_arg1_feat_func

from model_trainer.Implicit_Arg2_extractor.feature_functions \
    import all_features as _implicit_arg2_feat_func

import codecs


class DiscourseParser():
    def __init__(self, input_dataset, input_run):
        self.pdtb_parse = '%s/pdtb-parses.json' % input_dataset
        self.raw_path = '%s/raw' % input_dataset
        self.input_run = input_run
        self.relations = []
        self.explicit_relations = []
        self.non_explicit_relations = []


        self.documents = json.loads(codecs.open(self.pdtb_parse, encoding="utf-8", errors="ignore").read())
        
        self.parse_dict = self.documents

        pass

    def parse(self):

        ## add paragraph info
        parser_util.add_paragraph_info_for_parse(self.parse_dict, self.raw_path)


        # obtain all connectives in documents
        # conns_list: [(DocID, sent_index, conn_indices), ()..]
        conns_list = parser_util.get_all_connectives(self.documents)

        ''' 1.1 Connective classifier '''

        print "==> Connective classifier:"

        conn_clf_feature_function = _conn_clf_feature_function
        conn_clf_feat_path = config.PARSER_CONN_CLF_FEATURE
        conn_clf_model_path = config.CONNECTIVE_CLASSIFIER_MODEL
        conn_clf_model_output = config.PARSER_CONN_CLF_MODEL_OUTPUT

        # extract features for each connective
        parser_util.conn_clf_print_feature(self.parse_dict, conns_list, conn_clf_feature_function, conn_clf_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(conn_clf_feat_path, conn_clf_model_path, conn_clf_model_output)
        # read model output, obtain the discourse connectives
        conns_list = parser_util.conn_clf_read_model_output(conn_clf_model_output, conns_list)

        ''' 1.2 Arg1 position classifier '''

        print "\n==> Arg1 Position Classifier:"

        arg_position_feat_func = _arg_position_feature_function
        arg_position_feat_path = config.PARSER_ARG_POSITION_FEATURE
        arg_position_model_path = config.ARG_POSITION_CLASSIFIER_MODEL
        arg_position_model_output = config.PARSER_ARG_POSITION_MODEL_OUTPUT

        # extract features
        parser_util.arg_position_print_feature(self.parse_dict, conns_list, arg_position_feat_func, arg_position_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(arg_position_feat_path, arg_position_model_path, arg_position_model_output)
        # read model output
        # split the conns_list into SS_conns_list , PS_conns_list based on Arg1 Position Classifier
        SS_conns_list, PS_conns_list = parser_util.arg_position_read_model_output(arg_position_model_output, conns_list)

        ''' 1.3.1 SS Arguments Extractor '''

        print "\n==> SS Arguments Extractor:"

        # split the SS_conns_list into SS_conns_parallel_list, SS_conns_not_parallel_list
        # parallel connectives: if..then; either..or;...
        # not parallel connectives: and; or; ...
        SS_conns_parallel_list, SS_conns_not_parallel_list = parser_util.divide_SS_conns_list(SS_conns_list)

        constituent_feat_func = _constituent_feat_func
        constituent_feat_path = config.PARSER_CONSTITUENT_FEATURE
        constituent_model_path = config.NT_CLASSIFIER_MODEL
        constituent_model_output = config.PARSER_CONSTITUENT_MODEL_OUTPUT

        # connectives: connective object list;
        # one connective object for each item of SS_conns_not_parallel_list
        connectives = parser_util.get_all_connectives_for_NT(self.parse_dict, SS_conns_not_parallel_list)
        # extract features for each constituent of each connective
        parser_util.constituent_print_feature(self.parse_dict, connectives, constituent_feat_func, constituent_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(constituent_feat_path, constituent_model_path, constituent_model_output)
        # read model output, obtain two Arguments for each not parallel connective
        # SS_conns_not_parallel_list_args: [("SS", DocID, sent_index, conn_indices, Arg1, Arg2)]
        SS_conns_not_parallel_list_args = \
            parser_util.constituent_read_model_output(
                constituent_feat_path, constituent_model_output, self.parse_dict, SS_conns_not_parallel_list)
        # obtain two Arguments for each parallel connective by rules.
        SS_conns_parallel_list_args = parser_util.get_Args_for_SS_parallel_conns(self.parse_dict, SS_conns_parallel_list)

        ''' 1.3.2.1 PS Arg2 extractor '''

        print "\n==> PS Arg2 Extractor:"

        # initialize Arg1, Arg2 for PS:
        # previous sentence as Arg1, the sentence which contains the connective as Arg2
        PS_conns_list_args = parser_util.get_Args_for_PS_conns(self.parse_dict, PS_conns_list)

        PS_Arg2_feat_func = _ps_arg2_extractor_feat_func
        PS_Arg2_feat_path = config.PARSER_PS_ARG2_FEATURE
        PS_Arg2_model_path = config.PS_ARG2_CLASSIFIER_MODEL
        PS_Arg2_model_output = config.PARSER_PS_ARG2_MODEL_OUTPUT

        # extract features for PS Arg2 extractor
        parser_util.ps_arg2_extractor_print_feature \
            (self.parse_dict, PS_conns_list_args, PS_Arg2_feat_func, PS_Arg2_feat_path)

        # put feature file to corresponding model
        parser_util.put_feature_to_model(PS_Arg2_feat_path, PS_Arg2_model_path, PS_Arg2_model_output)

        # read model output, obtain Arg2 for PS
        PS_conns_list_args = parser_util.ps_arg2_extractor_read_model_output(
            PS_Arg2_feat_path, PS_Arg2_model_output, self.parse_dict, PS_conns_list_args)

        ''' 1.3.2.2 PS Arg1 extractor '''

        print "\n==> PS Arg1 Extractor:"

        PS_Arg1_feat_func = _ps_arg1_extractor_feat_func
        PS_Arg1_feat_path = config.PARSER_PS_ARG1_FEATURE
        PS_Arg1_model_path = config.PS_ARG1_CLASSIFIER_MODEL
        PS_Arg1_model_output = config.PARSER_PS_ARG1_MODEL_OUTPUT

        # extract features for PS Arg1 extractor
        parser_util.ps_arg1_extractor_print_feature \
            (self.parse_dict, PS_conns_list_args, PS_Arg1_feat_func, PS_Arg1_feat_path)

        # put feature file to corresponding model
        parser_util.put_feature_to_model(PS_Arg1_feat_path, PS_Arg1_model_path, PS_Arg1_model_output)

        # read model output, obtain Arg1 for PS
        PS_conns_list_args = parser_util.ps_arg1_extractor_read_model_output(
            PS_Arg1_feat_path, PS_Arg1_model_output, self.parse_dict, PS_conns_list_args)

        ''' 1.4 Explicit Sense Classifier '''

        print "\n==> Explicit Sense Classifier:"

        # all discourse connective: SS + PS
        #conns_list_args:[(source, DocID, sent_index, conn_indices, Arg1, Arg2)...]
        conns_list_args = SS_conns_not_parallel_list_args + SS_conns_parallel_list_args + PS_conns_list_args

        explicit_feat_func = _explicit_feat_func
        explicit_feat_path = config.PARSER_EXPLICIT_CLF_FEATURE
        explicit_model_path = config.EXPLICIT_CLASSIFIER_MODEL
        explicit_model_output = config.PARSER_EXPLICIT_CLF_MODEL_OUTPUT

        # extract features for Explicit Sense Classifier
        parser_util.explicit_clf_print_feature(self.parse_dict, conns_list_args, explicit_feat_func, explicit_feat_path)
        # put feature file into Explicit Sense Classifier model
        parser_util.put_feature_to_model(explicit_feat_path, explicit_model_path, explicit_model_output)
        # read model output, obtain the explicit sense for each connective
        # conns_args_sense_list: [(source, DocID, sent_index, conn_indices, Arg1, Arg2, sense)]
        conns_args_sense_list = parser_util.explicit_clf_read_model_output(explicit_model_output, conns_list_args)

        ''' explicit relation'''
        # obtain explicit relations
        self.explicit_relations = parser_util.get_explicit_relations(self.parse_dict, conns_args_sense_list)

        ''' 2.1 Non-Explicit Sense classifier: on original arguments '''

        print "\n==> Non-Explicit Sense classifier: on original arguments"

        # obtain all adjacent sentence pairs within each paragraph, but not identified in any Explicit relation
        # adjacent_non_exp_list: [(DocID,sent1_index,sent2_index) ]
        adjacent_non_exp_list = parser_util.get_adjacent_non_exp_list(self.parse_dict, PS_conns_list)

        # obtain non_explicit relation object list by adjacent_non_exp_list, no sense.
        self.non_explicit_relations = parser_util.get_non_explicit_relations(self.parse_dict, adjacent_non_exp_list)

        non_explicit_feat_func = _non_explicit_feat_func
        non_explicit_feat_path = config.PARSER_NON_EXPLICIT_CLF_FEATURE
        non_explicit_model_path = config.NON_EXPLICIT_CLASSIFIER_MODEL
        non_explicit_model_output = config.PARSER_NON_EXPLICIT_CLF_MODEL_OUTPUT

        # provide Non-Explicit relations with the Explicit relation context
        non_explicit_context_dict = parser_util.get_non_explicit_context_dict(self.explicit_relations)

        # extract non_explicit relation features
        parser_util.non_explicit_clf_print_feature \
            (self.parse_dict, self.non_explicit_relations, non_explicit_feat_func, non_explicit_context_dict, prev_context_conn, non_explicit_feat_path)

        # put feature file to corresponding model
        parser_util.put_feature_to_model(non_explicit_feat_path, non_explicit_model_path, non_explicit_model_output)

        # read model output, add sense for each non_explicit_relations
        self.non_explicit_relations = parser_util.non_explicit_read_model_output(non_explicit_model_output, self.parse_dict, self.non_explicit_relations)

        # divide the non_explicit_relations into EntRel_relations and Implicit_AltLex_relations
        # for Implicit_AltLex_relations (Non_EntRel relations in Non_Explicit), we build Implicit Arg1&Arg2 extractors to label Arg1&Arg2
        # for EntRel relations, we use previous sentence as Arg1 and the next one as Arg2.
        EntRel_relations, Implicit_AltLex_relations = parser_util.divide_non_explicit_relations(self.non_explicit_relations, self.parse_dict)

        ''' 2.2.1 Implicit Arg1 Extractor'''

        print "\n==> Implicit Arg1 Extractor:"

        implicit_arg1_feat_func = _implicit_arg1_feat_func
        implicit_arg1_feat_path = config.PARSER_IMPLICIT_ARG1_FEATURE
        implicit_arg1_model_path = config.IMPLICIT_ARG1_CLASSIFIER_MODEL
        implicit_arg1_model_output = config.PARSER_IMPLICIT_ARG1_MODEL_OUTPUT

        # extract features
        parser_util.implicit_arg1_print_feature \
            (self.parse_dict, Implicit_AltLex_relations, implicit_arg1_feat_func, implicit_arg1_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(implicit_arg1_feat_path, implicit_arg1_model_path, implicit_arg1_model_output)
        # read model output, obtain Arg1 for Implicit relations
        Implicit_AltLex_relations = parser_util.implicit_arg1_read_model_output(
            implicit_arg1_feat_path, implicit_arg1_model_output, self.parse_dict, Implicit_AltLex_relations)

        ''' 2.2.2 Implicit Arg2 Extractor'''

        print "\n==> Implicit Arg2 Extractor:"

        implicit_arg2_feat_func = _implicit_arg2_feat_func
        implicit_arg2_feat_path = config.PARSER_IMPLICIT_ARG2_FEATURE
        implicit_arg2_model_path = config.IMPLICIT_ARG2_CLASSIFIER_MODEL
        implicit_arg2_model_output = config.PARSER_IMPLICIT_ARG2_MODEL_OUTPUT

        # extract features
        parser_util.implicit_arg2_print_feature \
            (self.parse_dict, Implicit_AltLex_relations, implicit_arg2_feat_func, implicit_arg2_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(implicit_arg2_feat_path, implicit_arg2_model_path, implicit_arg2_model_output)
        # read model output, obtain Arg2 for Implicit relations
        Implicit_AltLex_relations = parser_util.implicit_arg2_read_model_output(
            implicit_arg2_feat_path, implicit_arg2_model_output, self.parse_dict, Implicit_AltLex_relations)

        # Non_Explicit relations
        self.non_explicit_relations = EntRel_relations + Implicit_AltLex_relations

        ''' 2.3 Non-Explicit Sense classifier: on refined arguments'''

        print "\n==> Non-Explicit Sense Classifier: on refined arguments"

        # change arguments from document offset to (sent_index, sent_offset).
        self.non_explicit_relations = parser_util.change_arg_doc_offset(self.non_explicit_relations, self.parse_dict)

        # extract features
        parser_util.non_explicit_clf_print_feature \
            (self.parse_dict, self.non_explicit_relations, non_explicit_feat_func, non_explicit_context_dict, prev_context_conn, non_explicit_feat_path)
        # put feature file to corresponding model
        parser_util.put_feature_to_model(non_explicit_feat_path, non_explicit_model_path, non_explicit_model_output)
        # read model output, add sense for each non_explicit_relations
        self.non_explicit_relations = parser_util.non_explicit_read_model_output(non_explicit_model_output, self.parse_dict, self.non_explicit_relations)

        # change arguments from (sent_index, sent_offset) to document offset
        self.non_explicit_relations = parser_util.change_arg_sent_offset(self.non_explicit_relations, self.parse_dict)

        ''' all discourse relations:  explicit_relations + non_explicit_relations'''
        # obtain all discourse relations generated by the discourse parser.
        self.relations = self.explicit_relations + self.non_explicit_relations






if __name__ == '__main__':
    # input_dataset = sys.argv[1]
    # input_run = sys.argv[2]
    # output_dir = sys.argv[3]

    input_dataset = config.CWD + "data/conll15-st-03-04-15-dev"
    input_run = ""
    output_dir = "data"

    parser = DiscourseParser(input_dataset, input_run)
    parser.parse()

    relations = parser.relations

    output = open('%s/output.json' % output_dir, 'w')
    for relation in relations:
        output.write('%s\n' % json.dumps(relation))
    output.close()