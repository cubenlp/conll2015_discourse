#coding:utf-8
import config, util, time
from feature import Feature
from connective_dict import Connectives_dict


class Connective:
    def __init__(self, DocID, sent_index, token_indices, name):
        self.relation_ID = None
        self.DocID = DocID
        self.sent_index = sent_index
        self.token_indices = token_indices#连接词在句子中的indices
        self.name = name
        self.Arg1_token_indices = None#句子中的indices
        self.Arg2_token_indices= None
        self.category = None #连接词的类别，subordinator , coordinator,adverbial"

        self.sense = None#连接词对应的sense

        self.features = None#连接词的features.

    #打印连接词的特征，输入到to_file, 使用多线程的方式。
    def print_features(self, document, pdtb_parse, to_file):
        self.document = document
        self.to_file =to_file
        self.pdtb_parse = pdtb_parse

        #所选择的特征
        feature_function_list = [self.CPOS_feature, self.pre_C_feature]

        util.run_multiple_threads(feature_function_list)

        pass

    '''---------------------------------------------'''
    '''   all the feature functions for connective  '''
    '''---------------------------------------------'''

    # C POS
    def CPOS_feature(self):
        feat_dict = {}
        #load the CPOS dict
        dict = Connectives_dict().cpos_dict
        #获取该连接词的 pos
        parse_dict = self.pdtb_parse.parse_dict
        for token_index in self.token_indices:
            pos_tag = parse_dict[self.DocID]["sentences"][self.sent_index]["words"][token_index][1]["PartOfSpeech"]
            if pos_tag in dict:
                feat_dict[dict[pos_tag]] = 1
        feature = Feature("CPOS", len(dict), feat_dict)
        return feature
    # pre word + C
    def pre_C_feature(self):
         # time.sleep(5)
         print "pre + C feature..."


