#coding:utf-8
from confusion_matrix import ConfusionMatrix, Alphabet


# gold_list = ['no', 'yes', 'no', 'yes', ...]
# predicted_list = ['yes', 'yes', 'no', 'yes', ...]
def compute_binary_eval_metric(predicted_list, gold_list, binary_alphabet):
    cm = ConfusionMatrix(binary_alphabet)
    for (predicted_span, gold_span) in zip( predicted_list, gold_list):
        cm.add(predicted_span, gold_span)
    return cm
