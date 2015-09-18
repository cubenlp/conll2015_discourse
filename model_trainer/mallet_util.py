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

def get_infoGain(svm_light_feat_file, info_gain_output_file, top_n):
    cmd = config.MALLET_PATH + \
              "/bin/mallet import-svmlight --input " + svm_light_feat_file + " --output "+ config.MALLET_FILE
    os.system(cmd)

    print "calculate info gain..."
    cmd = config.MALLET_PATH + \
        "/bin/vectors2info --input %s --print-infogain %d > %s" % (config.MALLET_FILE, top_n, info_gain_output_file)

    os.system(cmd)

def get_top_n_feat_dict_by_info_gain(svm_light_feat_file, info_gain_output_file, top_n, feat_dict, top_n_feat_dict_output):

    # 1. 生成 info gain 文件
    get_infoGain(svm_light_feat_file, info_gain_output_file, top_n)

    # 读文件，获取top n feature
    top_n_feat_indices = [] #从一开始计数的哦
    fin = open(info_gain_output_file)
    for line in fin:
        line = line.strip()
        if line == "":
            continue

        _, index = line.split()
        top_n_feat_indices.append(int(index))

    # index 到 feat 的映射
    index_to_feat_dict = {}
    dict_file = open(feat_dict)
    lines = [line.strip() for line in dict_file]
    for index, line in enumerate(lines):
        index_to_feat_dict[index+1] = line
    dict_file.close()

    # 写入文件
    fout = open(top_n_feat_dict_output, "w")
    for index in top_n_feat_indices:
        fout.write("%s\n" % (index_to_feat_dict[index]))
    fout.close()