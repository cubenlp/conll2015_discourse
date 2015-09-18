#coding:utf-8

# clause object
class Arg_Clauses():
    def __init__(self, relation_ID, Arg, DocID, sent_index, clauses):
        self.relation_ID = relation_ID
        self.Arg = Arg
        self.DocID = DocID
        self.sent_index = sent_index
        self.clauses = clauses # [([1,2,3],yes), ([4, 5],no), ]
        self.conn_indices = None
        self.conn_head_name = None