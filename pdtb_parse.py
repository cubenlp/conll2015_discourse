#coding:utf-8
import json, config
from sentence import check_connectives
from pdtb import PDTB
import pickle, os
from util import singleton
import sys
class PDTB_PARSE:
    def __init__(self, pdtb_parse_file_path, pdtb_file_path ,category):# category: train,dev,test...
        self.category = category
        self.pdtb = PDTB(pdtb_file_path, category)
        self.parse_dict = self.load_dict(pdtb_parse_file_path)
        self.disc_conns_dict = self.pdtb.exp_disc_conns_dict
        self.non_disc_conns_dict = self.get_non_disc_conns_dict()


    def load_dict(self, pdtb_parse_file_path):
        print "loading "+self.category+" pdtb parses..."
        parse_file = open(pdtb_parse_file_path)
        parse_dict = json.loads(parse_file.read())
        parse_file.close()
        return parse_dict

    #在parse中获取所有 non-disc-conn
    # dict[("DocID", sent_index)] = [[0], [1, 2]]
    def get_non_disc_conns_dict(self):

        # 判断该dict是否已经保存到硬盘
        if os.path.exists(config.PICKLE_NON_DISC_CONNS_PATH+"_"+self.category):
            return pickle.load( open( config.PICKLE_NON_DISC_CONNS_PATH+"_"+self.category, "rb" ) )

        non_disc_conns_dict = {}

        #0.加载 pdtb中的disc_conn dict
        # dict[("DocID", sent_index)] = [[0], [1, 2]]
        disc_conns_dict = self.pdtb.exp_disc_conns_dict

        #1. 识别每一句子中的连接词
        for DocID in self.parse_dict:
            for sent_index in range(len(self.parse_dict[DocID]["sentences"])):
                sent_tokens = [ word[0] for word in self.parse_dict[DocID]["sentences"][sent_index]["words"] ]
                #在sentence中标注连接词，[([2,6], 'for instance'), ....]
                for token_indices, conn_name in check_connectives(sent_tokens):
                    #2. 判断该连接词是否是disc_conn,
                    flag = 1
                    disc_conns = [[]]
                    if (DocID, sent_index) in disc_conns_dict.keys():
                        disc_conns = disc_conns_dict[(DocID, sent_index)]
                    for item in disc_conns:
                        if set(token_indices) & set(item) != set([]):
                            flag = 0
                            break
                    if flag == 1:
                        if (DocID, sent_index) in non_disc_conns_dict:
                            non_disc_conns_dict[(DocID, sent_index)].append(token_indices)
                        else:
                            non_disc_conns_dict[(DocID, sent_index)] = [token_indices]

        pickle.dump( non_disc_conns_dict, open( config.PICKLE_NON_DISC_CONNS_PATH+"_"+self.category, "wb" ) )

        return non_disc_conns_dict




# print PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH).non_disc_conns_dict

def add_NERTag_for_PDTB_parser(pdtb_parse_file_path):
    from nltk.tag.stanford import NERTagger
    import json
    nt = NERTagger(config.CWD + 'data/ner/english.muc.7class.distsim.crf.ser.gz', config.CWD + 'data/ner/stanford-ner.jar' )

    parse_file = open(pdtb_parse_file_path)
    parse_dict = json.loads(parse_file.read())

    total = float(len(parse_dict))
    t = 0
    for DocID in parse_dict:
        t += 1
        sys.stdout.flush()
        print "Process: %.2f%%\r" % (t/total * 100),
        for sent_index in range(len(parse_dict[DocID]["sentences"])):
            sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
            sent_tokens = [parse_dict[DocID]["sentences"][sent_index]["words"][index][0] for index in range(sent_length)]

            ner_tags = []
            for item in nt.tag(sent_tokens):
                ner_tags += item
            for i, (word, tag) in enumerate(ner_tags):
                parse_dict[DocID]["sentences"][sent_index]["words"][i][1]["NER_TAG"] = tag

    output = open(pdtb_parse_file_path + ".temp", 'w')
    output.write('%s\n' % json.dumps(parse_dict))
    output.close()



if __name__ == "__main__":
    # add_NERTag_for_PDTB_parser(config.PARSERS_TRAIN_PATH_JSON)
    # add_NERTag_for_PDTB_parser(config.PARSERS_DEV_PATH_JSON)
    train_pdtb_parse = PDTB_PARSE(config.PARSERS_TRAIN_PATH_JSON, config.PDTB_TRAIN_PATH, config.TRAIN)
    dev_pdtb_parse =  PDTB_PARSE(config.PARSERS_DEV_PATH_JSON, config.PDTB_DEV_PATH, config.DEV)
    pass