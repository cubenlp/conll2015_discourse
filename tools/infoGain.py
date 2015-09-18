#coding:utf-8
from math import log
import operator
from sklearn.datasets import load_svmlight_file

def production_rules():
    # production rules
    mallet_util.get_top_n_feat_dict_by_info_gain \
        (config.FEATURE_SELECTION_PRODUCTION_RULES,
         config.FEATURE_SELECTION_PRODUCTION_RULES_INFOGAIN,
         165,
         config.NON_EXPLICIT_DICT_PRODUCTION_RULES,
         config.FEATURE_SELECTION_DICT_TOP_N_PRODUCTION_RULES

    )

    #Both_QP-->$ CD CD
    fin = open(config.FEATURE_SELECTION_DICT_TOP_N_PRODUCTION_RULES)
    rules = []
    for line in fin:
        line = line.strip()
        _, rule = line.split("_")
        rules.append(rule)
    rules = list(set(rules))

    production_rules = ["Arg1_%s" % rule for rule in rules] + \
                       ["Arg2_%s" % rule for rule in rules] + \
                       ["Both_%s" % rule for rule in rules]

    fout = open(config.FEATURE_SELECTION_DICT_TOP_N_PRODUCTION_RULES, "w")
    fout.write("\n".join(production_rules))
    fout.close()

if __name__ == "__main__":
    import config, util
    from model_trainer import mallet_util

    # production rules
    mallet_util.get_top_n_feat_dict_by_info_gain \
        (config.FEATURE_SELECTION_BROWN_CLUSTER,
         config.FEATURE_SELECTION_BROWN_CLUSTER_INFOGAIN,
         50000,
         config.NON_EXPLICIT_DICT_BROWN_CLUSTER_PAIRS,
         config.FEATURE_SELECTION_DICT_TOP_N_BROWN_CLUSTER

    )

