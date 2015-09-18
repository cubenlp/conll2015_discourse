#coding:utf-8
class Feature:
    #featDict : 3:1, 10:0.5, 7:1
    def __init__(self,name, dimension, feat_dict):
        self.name = name #特征名称
        self.dimension = dimension #维度
        self.feat_string = self.featDict2String(feat_dict) #特征: "3:1 7:1 10:0.5"


    def featDict2String(self, feat_dict):
        #按键值排序
        list = [str(key)+":"+str(feat_dict[key]) for key in sorted(feat_dict.keys())]
        return " ".join(list)



