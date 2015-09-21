#coding:utf-8
import operator
import config, os, util

def get_mallet_gold_list(file_path):
    gold_list = []
    for line in open(file_path):
        gold = line.strip().split("\t")[0]
        gold_list.append(gold)
    return gold_list

def get_mallet_predicted_list(file_path):
    predicted_dict_list = read_mallet_output(file_path)
    predicted_list = []
    for predicted_dict in predicted_dict_list:
        sort_label = sorted(predicted_dict.iteritems(), key=operator.itemgetter(1),reverse = True)
        predicted_list.append(sort_label[0][0])
    return predicted_list

def read_mallet_output(file_path):
        predicted_dict_list = []
        for line in open(file_path):
            fields = line.rstrip().split("\t")[1:]
            dict = {}
            for i in range(len(fields)):
                if i % 2 == 0:
                    dict[fields[i]] = float(fields[i+1])
            predicted_dict_list.append(dict)
        return predicted_dict_list
