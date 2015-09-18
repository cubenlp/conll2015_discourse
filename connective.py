#coding:utf-8
import config, util, time
from feature import Feature
from connective_dict import Connectives_dict


class Connective:
    def __init__(self, DocID, sent_index, token_indices, name):
        self.relation_ID = None
        self.DocID = DocID
        self.sent_index = sent_index
        self.token_indices = token_indices# the token indices of connective in sentence
        self.name = name
        self.Arg1_token_indices = None
        self.Arg2_token_indices= None
        self.category = None # connective category，subordinator , coordinator,adverbial"

        self.sense = None

        self.features = None




