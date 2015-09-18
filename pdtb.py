#coding:utf-8
import json, config, os, pickle
from util import singleton
from model_trainer.connective_classifier.conn_head_mapper import ConnHeadMapper
from connective import Connective

class PDTB:
    def __init__(self, pdtb_file_path, category):
        self.category = category
        self.relations = self.load_pdtb(pdtb_file_path)
        self.exp_disc_conns_dict = self.get_exp_disc_conns_dict()#dict[("DocID", sent_index)] = [[0], [1, 2]]

        #dict[("DocID", sent_index)] = [[0],[1,2]]
        self.SS_conns_dict, self.PS_conns_dict= self.get_SS_PS_conns_dict() # arg1,arg2在相同句子中 # arg1 在 arg2 前面

        self.IPS_relations = self.get_IPS_relations()
        self.SS_relations = self.get_SS_relations()
        # 用于implicit 的 context
        # dict([DocID, sent1_index, sent2_index]) = (conn, sense)
        self.implicit_context_dict = self.get_implicit_context_dict(self.IPS_relations + self.SS_relations)


        # arg1,arg2为同一个句子，连接词为从属连接词
        self.subordinating_conns_SS = []
        self.coordinating_conns_SS = []
        self.adverbial_conns_SS = []

        #arg1,arg2在同一个句子了, training: 8880 vs 5842
        self.IPS_conns, self.one_SS_conns, self.not_one_SS_conns = self.get_one_SS_conns_dict()

        self.one_SS_conns_not_parallel, self.one_SS_conns_parallel = self.divide_to_parallel_and_not(self.one_SS_conns)

        # for explicit classifier
        self.conns_list = self.get_conns_list()


        self.get_conns_SS_by_category()

        #non-explicit relations
        self.non_explicit_relations, self.explicit_relations = self.get_non_explicit_relations()



    def get_conns_list(self):
        conns_list = []
        for relation in self.relations:
            if relation["Type"] =="Explicit":
                DocID = relation["DocID"]
                sent_index = relation["Connective"]["TokenList"][0][3]
                conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]



                #需要将获取语篇连接词的头
                raw_connective = relation["Connective"]["RawText"]
                chm = ConnHeadMapper()
                conn_head, indices = chm.map_raw_connective(raw_connective)
                conn_head_indices = [conn_token_indices[index] for index in indices]

                conn = Connective(DocID, sent_index, conn_head_indices, conn_head)
                conn.relation_ID = relation["ID"]
                conn.sense = relation["Sense"]

                conns_list.append(conn)

        return conns_list






    def get_conns_SS_by_category(self):

        conn_category_dict = self.get_conn_category_dict()

        c = 0


        for relation in self.relations:
            if relation["Type"] =="Explicit":

                DocID = relation["DocID"]
                sent_index = relation["Connective"]["TokenList"][0][3]
                conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
                Arg1_token_indices = [item[4] for item in relation["Arg1"]["TokenList"]]
                Arg2_token_indices = [item[4] for item in relation["Arg2"]["TokenList"]]


                #需要将获取语篇连接词的头
                raw_connective = relation["Connective"]["RawText"]
                chm = ConnHeadMapper()
                conn_head, indices = chm.map_raw_connective(raw_connective)
                conn_head_indices = [conn_token_indices[index] for index in indices]

                Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])




                # if conn_head == "either or":
                #     conn_head_indices = [conn_head_indices[-1]]
                # if conn_head == "if then":
                #     # print DocID, sent_index
                #     conn_head_indices = [conn_head_indices[-1]]
                #
                # if conn_head == "so":
                #     print "\n" + "--"*8 + "\n"
                #     print DocID, sent_index
                #     # print relation["Connective"]["TokenList"][0][4],\
                #     #     [item[4] for item in relation["Arg1"]["TokenList"]],\
                #     #     relation["Connective"]["TokenList"][1][4], \
                #     # [item[4] for item in relation["Arg2"]["TokenList"]]
                #     print [item[4] for item in relation["Arg1"]["TokenList"]],
                #     print [item[4] for item in relation["Arg2"]["TokenList"]],

                #
                #     conn_head_indices = [conn_head_indices[-1]]
                # if conn_head == "on the one hand on the other hand":
                #     conn_head_indices = conn_head_indices[4:]




                # if set(Arg2_sent_indices) >= set(Arg1_sent_indices) or Arg1_sent_indices[-1] < Arg2_sent_indices[0]:
                #     c += 1

                if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:#只考虑句子长度为1
                    if set(Arg2_sent_indices) == set(Arg1_sent_indices) :#SS
                        conn = Connective(DocID, sent_index, conn_head_indices, conn_head)
                        conn.relation_ID = relation["ID"]
                        conn.Arg1_token_indices = Arg1_token_indices
                        conn.Arg2_token_indices = Arg2_token_indices

                        # 1. 判断连接词类别
                        category = conn_category_dict[conn_head]

                        if config.adverbial == category:
                            conn.category = config.adverbial
                            self.adverbial_conns_SS.append(conn)

                        if config.Subordinator == category:
                            conn.category = config.Subordinator
                            self.subordinating_conns_SS.append(conn)

                        if config.Coordinator == category:
                            conn.category = config.Coordinator
                            self.coordinating_conns_SS.append(conn)

        # print c




    def get_conn_category_dict(self):
        dict = {}
        file = open(config.CONNECTIVE_CATEGORY_PATH)
        lines = [line.strip() for line in file.readlines()]
        for line in lines:
            list = line.split("#")
            conn = list[0].strip()
            category = list[1].strip()
            dict[conn] = category
        return dict

    def get_SS_PS_conns_dict(self):

        SS_conns_dict = {}
        PS_conns_dict = {}

        c1 = 0
        c2 = 0

        for relation in self.relations:
            if relation["Type"] =="Explicit":
                DocID = relation["DocID"]
                sent_index = relation["Connective"]["TokenList"][0][3]
                conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
                #需要将获取语篇连接词的头
                raw_connective = relation["Connective"]["RawText"]
                chm = ConnHeadMapper()
                conn_head, indices = chm.map_raw_connective(raw_connective)
                conn_head_indices = [conn_token_indices[index] for index in indices]





                Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])

                # if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:#只考虑句子长度为1
                if set(Arg2_sent_indices) >= set(Arg1_sent_indices) :#SS
                    c1 += 1
                    if (DocID, sent_index) in SS_conns_dict:
                        SS_conns_dict[(DocID, sent_index)].append(conn_head_indices)
                    else:
                        SS_conns_dict[(DocID, sent_index)] = [conn_head_indices]

                else:
                    if Arg1_sent_indices[-1] < Arg2_sent_indices[0] :# PS
                        c2 += 1
                        if (DocID, sent_index) in PS_conns_dict:
                            PS_conns_dict[(DocID, sent_index)].append(conn_head_indices)
                        else:
                            PS_conns_dict[(DocID, sent_index)] = [conn_head_indices]

        print "Explicit: SS: %d.\tPS:%d" % (c1, c2)
        return SS_conns_dict, PS_conns_dict




    def load_pdtb(self, pdtb_file_path):
        print "loading "+self.category+" pdtb file..."
        pdtb_file = open(pdtb_file_path)
        relations = [json.loads(x) for x in pdtb_file]
        pdtb_file.close()
        return relations

    #从pdtb数据集中获取语篇连接词
    # 构成字典：dict[("DocID", sent_index)] = [[0], [1, 2]]
    def get_exp_disc_conns_dict(self):
        #判断该dict是否已经保存到硬盘
        if os.path.exists(config.PICKLE_DISC_CONNS_PATH+"_"+self.category):
            return pickle.load( open(config.PICKLE_DISC_CONNS_PATH+"_"+self.category, "rb" ) )

        exp_disc_conns_dict = {}
        for relation in self.relations:
            if relation["Type"] == "Explicit":
                DocID = relation["DocID"]
                sent_index = relation["Connective"]["TokenList"][0][3]
                conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
                #需要将获取语篇连接词的头
                raw_connective = relation["Connective"]["RawText"]
                chm = ConnHeadMapper()
                conn_head, indices = chm.map_raw_connective(raw_connective)
                conn_head_indices = [conn_token_indices[index] for index in indices]

                if (DocID, sent_index) in exp_disc_conns_dict:
                    exp_disc_conns_dict[(DocID, sent_index)].append(conn_head_indices)
                else:
                    exp_disc_conns_dict[(DocID, sent_index)] = [conn_head_indices]

        pickle.dump( exp_disc_conns_dict, open( config.PICKLE_DISC_CONNS_PATH+"_"+self.category, "wb" ) )

        return exp_disc_conns_dict


    def get_one_SS_conns_dict(self):
        #直接前面一个句子！
        IPS_conns = []

        one_SS_conns = []
        not_one_SS_conns = []

        for relation in self.relations:
            if relation["Type"] =="Explicit":

                DocID = relation["DocID"]
                sent_index = relation["Connective"]["TokenList"][0][3]
                conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]
                Arg1_token_indices = [item[4] for item in relation["Arg1"]["TokenList"]]
                Arg2_token_indices = [item[4] for item in relation["Arg2"]["TokenList"]]


                #需要将获取语篇连接词的头
                raw_connective = relation["Connective"]["RawText"]
                chm = ConnHeadMapper()
                conn_head, indices = chm.map_raw_connective(raw_connective)
                conn_head_indices = [conn_token_indices[index] for index in indices]

                Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])


                conn = Connective(DocID, sent_index, conn_head_indices, conn_head)
                conn.relation_ID = relation["ID"]
                conn.Arg1_token_indices = Arg1_token_indices
                conn.Arg2_token_indices = Arg2_token_indices

                if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:#只考虑句子长度为1
                    if set(Arg2_sent_indices) == set(Arg1_sent_indices) :#SS
                        one_SS_conns.append(conn)
                    else:
                        not_one_SS_conns.append(conn)
                        #Arg1 为前面的一个句子
                        if Arg1_sent_indices[0] == Arg2_sent_indices[0] - 1:
                            IPS_conns.append(conn)

                else:
                    not_one_SS_conns.append(conn)
        return IPS_conns, one_SS_conns, not_one_SS_conns

    def divide_to_parallel_and_not(self, one_SS_conns):
        one_SS_conns_not_parallel = []
        one_SS_conns_parallel = []
        for connective in one_SS_conns:
            if connective.name == "if then" or connective.name == "either or" \
                or connective.name == "neither nor" or connective.name == "on the one hand on the other hand":
                one_SS_conns_parallel.append(connective)
            else:
                one_SS_conns_not_parallel.append(connective)

        return one_SS_conns_not_parallel, one_SS_conns_parallel


        # print c

    # 获取所有的非显性语篇关系
    def get_non_explicit_relations(self):
        explicit_relations = []
        non_explicit_relations = []
        for relation in self.relations:
            if relation["Type"] != "Explicit":
                non_explicit_relations.append(relation)
            else:
                explicit_relations.append(relation)
        return non_explicit_relations, explicit_relations

    def get_IPS_relations(self):
        IPS_relations = []
        for relation in self.relations:
            if relation["Type"] == "Explicit":
                Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
                conn_sent_indices = sorted([item[3] for item in relation["Connective"]["TokenList"]])
                if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:#只考虑句子长度为1
                    if Arg1_sent_indices[0] == Arg2_sent_indices[0] - 1 and set(conn_sent_indices) <= set(Arg2_sent_indices):
                            IPS_relations.append(relation)

        return IPS_relations

    def get_SS_relations(self):
        SS_relations = []
        for relation in self.relations:
            if relation["Type"] == "Explicit":
                Arg1_sent_indices = sorted([item[3] for item in relation["Arg1"]["TokenList"]])
                Arg2_sent_indices = sorted([item[3] for item in relation["Arg2"]["TokenList"]])
                conn_sent_indices = sorted([item[3] for item in relation["Connective"]["TokenList"]])
                if len(set(Arg1_sent_indices)) == 1 and len(set(Arg2_sent_indices)) == 1:#只考虑句子长度为1
                    if Arg1_sent_indices[0] == Arg2_sent_indices[0] and set(conn_sent_indices) <= set(Arg2_sent_indices):
                            SS_relations.append(relation)

        return SS_relations

    # 只有SS ,PS
    # dict([DocID, sent1_index, sent2_index]) = [(conn_indices_string, conn, sense)]
    def get_implicit_context_dict(self, relations):
        context_dict = {}
        for relation in relations:
            DocID = relation["DocID"]

            sent1_index = relation["Arg1"]["TokenList"][0][3]
            sent2_index = relation["Arg2"]["TokenList"][0][3]
            conn_sent_index = relation["Connective"]["TokenList"][0][3]

            conn_token_indices = [item[4] for item in relation["Connective"]["TokenList"]]

            #需要将获取语篇连接词的头
            raw_connective = relation["Connective"]["RawText"]
            chm = ConnHeadMapper()
            conn_head, conn_indices = chm.map_raw_connective(raw_connective)
            conn_head_indices = [conn_token_indices[index] for index in conn_indices]

            conn_indices_string = " ".join([str(x) for x in conn_head_indices])

            sense = relation["Sense"][0]

            if (DocID, sent1_index, sent2_index) not in context_dict:
                context_dict[(DocID, sent1_index, sent2_index)] = []
            context_dict[(DocID, sent1_index, sent2_index)].append((conn_indices_string,conn_head, sense))

        return context_dict



# #
if __name__ == "__main__":
    pdtb_train = PDTB(config.PDTB_TRAIN_PATH, config.TRAIN)
    # pdtb_train = PDTB(config.PDTB_DEV_PATH, config.DEV)
    print len(pdtb_train.one_SS_conns)
    print len(pdtb_train.not_one_SS_conns)
    print len(pdtb_train.non_explicit_relations)
    print "IPS_relations :" + str(len(pdtb_train.IPS_relations))
    print "SS_relations : " + str(len(pdtb_train.SS_relations))
    print len(pdtb_train.implicit_context_dict)
    print pdtb_train.implicit_context_dict
    # print len(pdtb_train.subordinating_conns_SS)/14705.0
    # print len(pdtb_train.coordinating_conns_SS)/14705.0
    # print len(pdtb_train.adverbial_conns_SS)/14705.0

