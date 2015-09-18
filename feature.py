#coding:utf-8
class Feature:
    #featDict : 3:1, 10:0.5, 7:1
    def __init__(self,name, dimension, feat_dict):
        self.name = name # feature name
        self.dimension = dimension # feature dimension
        self.feat_string = self.featDict2String(feat_dict) # feature string: "3:1 7:1 10:0.5"


    def featDict2String(self, feat_dict):
        # sort by key...
        list = [str(key)+":"+str(feat_dict[key]) for key in sorted(feat_dict.keys())]
        return " ".join(list)



