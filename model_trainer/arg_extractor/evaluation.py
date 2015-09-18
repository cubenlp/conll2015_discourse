from model_trainer.mallet_util import *
from model_trainer.evaluation import compute_binary_eval_metric
from model_trainer.confusion_matrix import Alphabet
import config

def get_evaluation(result_file_path):
    gold_list = get_mallet_gold_list(result_file_path)
    predicted_list = get_mallet_predicted_list(result_file_path)
    alphabet = Alphabet()
    alphabet.add('Arg1_node')
    alphabet.add('Arg2_node')
    alphabet.add('NONE')
    cm = compute_binary_eval_metric(
			 predicted_list, gold_list, alphabet)
    return cm

#  target|arg1_prob|arg2_prob|relation_ID|DocID|sent_index|node_location

def get_evaluation_file():
    dev_feat_file = open(config.ARG_EXTRACTOR_DEV_FEATURE_OUTPUT_PATH)
    dev_output = open(config.ARG_EXTRACTOR_DEV_OUTPUT_PATH)
    dev_feat_lines = [line.strip() for line in dev_feat_file]
    dev_output_lines = [line.strip() for line in dev_output]

    lines = []
    for output_line, feat_line in zip(dev_output_lines, dev_feat_lines):
        target = output_line.split("\t")[0]
        arg1_prob = output_line.split("\t")[4]
        arg2_prob = output_line.split("\t")[6]
        line = "%s|%s|%s|%s" % (target, arg1_prob, arg2_prob, feat_line.split("#")[1].strip())
        lines.append(line)
    fout = open(config.ARG_EXTRACTOR_DEV_EVALUATION_PATH, "w")
    fout.write("\n".join(lines))
    fout.close()

def get_arg1_arg2_node_evaluation():
    get_evaluation_file()

    fin = open(config.ARG_EXTRACTOR_DEV_EVALUATION_PATH)
    lines = [line.strip() for line in fin]
    dict = {}

    for line in lines:
        target, arg1_node_prob, arg2_node_prob, relation_ID, DocID, sent_index, node_location = line.split("|")
        if relation_ID not in dict:
            dict[relation_ID] = [(target, arg1_node_prob, arg2_node_prob, DocID, sent_index, node_location)]
        else:
            dict[relation_ID].append((target, arg1_node_prob, arg2_node_prob, DocID, sent_index, node_location))


    arg1_node_right_count = 0
    arg2_node_right_count = 0
    arg1_and_arg2_right_count = 0
    for relation_ID in dict.keys():
        list = dict[relation_ID]
        arg1_prob_list = [float(item[1]) for item in list]
        arg2_prob_list = [float(item[2]) for item in list]

        arg1_index = arg1_prob_list.index(max(arg1_prob_list))
        arg2_index = arg2_prob_list.index(max(arg2_prob_list))

        if list[arg1_index][0] == "Arg1_node":
            arg1_node_right_count += 1
        if list[arg2_index][0] == "Arg2_node":
            arg2_node_right_count += 1
        if list[arg1_index][0] == "Arg1_node" and list[arg2_index][0] == "Arg2_node":
            arg1_and_arg2_right_count += 1

    print "arg1 count: %d" % (arg1_node_right_count)
    print "arg2 count: %d" % (arg2_node_right_count)
    print "arg1 and arg2 count: %d" % (arg1_and_arg2_right_count)
    print "sum: %d" % (len(dict))

    print "arg1 F1: %.2f%%" % (arg1_node_right_count/float(len(dict))*100)
    print "arg2 F1: %.2f%%" % (arg2_node_right_count/float(len(dict))*100)
    print "arg1 and arg2 F1: %.2f%%" % (arg1_and_arg2_right_count/float(len(dict))*100)


# get_arg1_arg2_node_evaluation()


