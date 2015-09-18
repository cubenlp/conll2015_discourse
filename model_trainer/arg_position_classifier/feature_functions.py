#coding:utf-8
from arg_position_dict import Arg_position_dict
import arg_position_dict_util as dict_util
from feature import Feature
import util

def all_features(parse_dict, DocID, sent_index, conn_indices):
    ''' feat dict '''
    feat_dict_CString = {}
    feat_dict_CPOS = {}
    feat_dict_prev1 = {}
    feat_dict_prev1POS = {}
    feat_dict_prev1_C = {}
    feat_dict_prev1POS_CPOS = {}
    feat_dict_prev2 = {}
    feat_dict_prev2POS = {}
    feat_dict_prev2_C = {}
    feat_dict_prev2POS_CPOS = {}

    feat_dict_next1 = {}
    feat_dict_next1POS = {}
    feat_dict_next1_C = {}
    feat_dict_next1POS_CPOS = {}
    feat_dict_next2 = {}
    feat_dict_next2POS = {}
    feat_dict_next2_C = {}
    feat_dict_next2POS_CPOS = {}

    ''' load dict '''
    dict_CString = Arg_position_dict().dict_CString
    dict_CPOS = Arg_position_dict().dict_CPOS
    dict_prev1 = Arg_position_dict().dict_prev1
    dict_prev1POS = Arg_position_dict().dict_prev1POS
    dict_prev1_C = Arg_position_dict().dict_prev1_C
    dict_prev1POS_CPOS = Arg_position_dict().dict_prev1POS_CPOS
    dict_prev2 = Arg_position_dict().dict_prev2
    dict_prev2POS = Arg_position_dict().dict_prev2POS
    dict_prev2_C = Arg_position_dict().dict_prev2_C
    dict_prev2POS_CPOS = Arg_position_dict().dict_prev2POS_CPOS

    dict_conn_to_root_path = Arg_position_dict().dict_conn_to_root_path

    dict_next1 = Arg_position_dict().dict_next1
    dict_next1POS = Arg_position_dict().dict_next1POS
    dict_next1_C = Arg_position_dict().dict_next1_C
    dict_next1POS_CPOS = Arg_position_dict().dict_next1POS_CPOS
    dict_next2 = Arg_position_dict().dict_next2
    dict_next2POS = Arg_position_dict().dict_next2POS
    dict_next2_C = Arg_position_dict().dict_next2_C
    dict_next2POS_CPOS = Arg_position_dict().dict_next2POS_CPOS

    ''' feature '''
    C_String = dict_util.get_C_String(parse_dict, DocID, sent_index, conn_indices)
    CPOS = dict_util.get_CPOS(parse_dict, DocID, sent_index, conn_indices)
    prev1 = dict_util.get_prev1(parse_dict, DocID, sent_index, conn_indices)
    prev1POS = dict_util.get_prev1POS(parse_dict, DocID, sent_index, conn_indices)
    prev2 = dict_util.get_prev2(parse_dict, DocID, sent_index, conn_indices)
    prev2POS = dict_util.get_prev2POS(parse_dict, DocID, sent_index, conn_indices)

    prev1_C = "%s|%s" % (prev1, C_String)
    prev1POS_CPOS = "%s|%s" % (prev1POS, CPOS)

    prev2_C = "%s|%s" % (prev2, C_String)
    prev2POS_CPOS = "%s|%s" % (prev2POS, CPOS)

    next1, next1POS = dict_util.get_next1_next1POS(parse_dict, DocID, sent_index, conn_indices)
    next2, next2POS = dict_util.get_next2_next2POS(parse_dict, DocID, sent_index, conn_indices)

    next1_C = "%s|%s" % (C_String, next1)
    next1POS_CPOS = "%s|%s" % (CPOS, next1POS)

    next2_C = "%s|%s" % (C_String, next2)
    next2POS_CPOS = "%s|%s" % (CPOS, next2POS)

    conn_to_root_path = dict_util.get_conn_to_root_path(parse_dict, DocID, sent_index, conn_indices)


    features = []
    features.append(get_feature(feat_dict_CString, dict_CString, C_String))
    features.append(C_Position_feature(parse_dict, DocID, sent_index, conn_indices))# position feature
    features.append(get_feature(feat_dict_CPOS, dict_CPOS, CPOS))
    features.append(get_feature(feat_dict_prev1, dict_prev1, prev1))
    features.append(get_feature(feat_dict_prev1POS, dict_prev1POS, prev1POS))
    features.append(get_feature(feat_dict_prev1_C, dict_prev1_C, prev1_C))
    features.append(get_feature(feat_dict_prev1POS_CPOS, dict_prev1POS_CPOS, prev1POS_CPOS))
    features.append(get_feature(feat_dict_prev2, dict_prev2, prev2))
    features.append(get_feature(feat_dict_prev2POS, dict_prev2POS, prev2POS))
    features.append(get_feature(feat_dict_prev2_C, dict_prev2_C, prev2_C))
    features.append(get_feature(feat_dict_prev2POS_CPOS, dict_prev2POS_CPOS, prev2POS_CPOS))

    # features.append(get_feature(feat_dict_next1, dict_next1, next1))
    # features.append(get_feature(feat_dict_next1POS, dict_next1POS, next1POS))
    # features.append(get_feature(feat_dict_next1_C, dict_next1_C, next1_C))
    features.append(get_feature(feat_dict_next1POS_CPOS, dict_next1POS_CPOS, next1POS_CPOS))
    features.append(get_feature(feat_dict_next2, dict_next2, next2))
    # features.append(get_feature(feat_dict_next2POS, dict_next2POS, next2POS))
    # features.append(get_feature(feat_dict_next2_C, dict_next2_C, next2_C))
    # features.append(get_feature(feat_dict_next2POS_CPOS, dict_next2POS_CPOS, next2POS_CPOS))

    features.append(get_feature_by_feat(dict_conn_to_root_path, conn_to_root_path))


    # C_String,
    # conn_to_root_path,
    # prev1_C,
    # prev2POS_CPOS,
    # prev1POS,
    # CPOS,
    # C_Position_feature,
    # next1POS_CPOS,
    # prev2,
    # prev1POS_CPOS,
    # next2,
    # prev2_C,
    # prev1,
    # prev2POS,



    return util.mergeFeatures(features)

# C 在句子中的位置
# 0~1/5: start
# 1/5~4/5 : middle
# 4/5~5/5 : end
def C_Position_feature(parse_dict, DocID, sent_index, conn_indices):
    feat_dict = {}
    dict = {"start": 1, "middle": 2 ,"end": 3}
    sent_length = len(parse_dict[DocID]["sentences"][sent_index]["words"])
    position = float(conn_indices[0])/float(sent_length)
    if position <= 0.2:
        feat = "start"
    elif position >= 0.8:
        feat = "end"
    else:
        feat = "middle"

    return get_feature(feat_dict, dict, feat)

def get_feature(feat_dict, dict, feat):
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_list(list):
    feat_dict = {}
    for index, item in enumerate(list):
        if item != 0:
            feat_dict[index+1] = item
    return Feature("", len(list), feat_dict)


def get_feature_by_feat(dict, feat):
    feat_dict = {}
    if feat in dict:
        feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)

def get_feature_by_feat_list(dict, feat_list):
    feat_dict = {}
    for feat in feat_list:
        if feat in dict:
            feat_dict[dict[feat]] = 1
    return Feature("", len(dict), feat_dict)