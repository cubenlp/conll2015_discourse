# -*- coding: utf-8 -*-
"""A collection of data structures that are particularly
useful for developing and improving a classifier
"""

import numpy, json

class ConfusionMatrix(object):
    """Confusion matrix for evaluating a classifier

    For more information on confusion matrix en.wikipedia.org/wiki/Confusion_matrix"""

    INIT_NUM_CLASSES = 100
    def __init__(self, alphabet=None):
        if alphabet is None:
            self.alphabet = Alphabet()
            self.matrix = numpy.zeros((self.INIT_NUM_CLASSES, self.INIT_NUM_CLASSES))
        else:
            self.alphabet = alphabet
            num_classes = alphabet.size()
            self.matrix = numpy.zeros((num_classes,num_classes))

    def __iadd__(self, other):
        self.matrix += other.matrix
        return self

    def add(self, prediction, true_answer):
        """Add one data point to the confusion matrix

        If prediction is an integer, we assume that it's a legitimate index
        on the confusion matrix.

        If prediction is a string, then we will do the look up to
        map to the integer index for the confusion matrix.

        """
        if type(prediction) == int and type(true_answer) == int:
            self.matrix[prediction, true_answer] += 1
        else:
            self.alphabet.add(prediction)
            self.alphabet.add(true_answer)
            prediction_index = self.alphabet.get_index(prediction)
            true_answer_index = self.alphabet.get_index(true_answer)
            self.matrix[prediction_index, true_answer_index] += 1
            #XXX: this will fail if the prediction_index is greater than
            # the initial capacity. I should grow the matrix if this crashes


    def add_list(self, predictions, true_answers):
        for p, t in zip(predictions, true_answers):
            self.add(p, t)

    def compute_average_f1(self):
        precision = numpy.zeros(self.alphabet.size())
        recall = numpy.zeros(self.alphabet.size())
        f1 = numpy.zeros(self.alphabet.size())

        # computing precision, recall, and f1
        for i in xrange(self.alphabet.size()):
            precision[i] = self.matrix[i,i] / sum(self.matrix[i,:])
            recall[i] = self.matrix[i,i] / sum(self.matrix[:,i])
            if precision[i] + recall[i] != 0:
                f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            else:
                f1[i] = 0
        return numpy.mean(f1)

    def print_matrix(self):
        num_classes = self.alphabet.size()
        #header for the confusion matrix
        header = [' '] + [self.alphabet.get_label(i) for i in xrange(num_classes)]
        rows = []
        #putting labels to the first column of rhw matrix
        for i in xrange(num_classes):
            row = [self.alphabet.get_label(i)] + [str(self.matrix[i,j]) for j in xrange(num_classes)]
            rows.append(row)
        print "row = predicted, column = truth"
        print matrix_to_string(rows, header)

    def get_matrix(self):
        num_classes = self.alphabet.size()
        #header for the confusion matrix
        header = [' '] + [self.alphabet.get_label(i) for i in xrange(num_classes)]
        rows = []
        #putting labels to the first column of rhw matrix
        for i in xrange(num_classes):
            row = [self.alphabet.get_label(i)] + [str(self.matrix[i,j]) for j in xrange(num_classes)]
            rows.append(row)
        return "row = predicted, column = truth\n" + matrix_to_string(rows, header)

    def get_prf(self, class_name):
        index = self.alphabet.get_index(class_name)
        precision = self.matrix[index, index] / sum(self.matrix[index, :])
        recall = self.matrix[index, index] / sum(self.matrix[:, index])
        f1 = (2 * precision * recall) / (precision + recall)
        return (precision, recall, f1)




    def print_summary(self):
        correct = 0

        precision = numpy.zeros(self.alphabet.size())
        recall = numpy.zeros(self.alphabet.size())
        f1 = numpy.zeros(self.alphabet.size())

        lines = []
        # computing precision, recall, and f1
        for i in xrange(self.alphabet.size()):
            precision[i] = self.matrix[i,i] / sum(self.matrix[i,:])
            recall[i] = self.matrix[i,i] / sum(self.matrix[:,i])
            if precision[i] + recall[i] != 0:
                f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            else:
                f1[i] = 0
            correct += self.matrix[i,i]
            label = self.alphabet.get_label(i)
            lines.append( '%s \tprecision %f \trecall %f\t F1 %f' %\
                    (label, precision[i], recall[i], f1[i]))
        lines.append( '* Overall accuracy rate = %f' %(correct / sum(sum(self.matrix[:,:]))))
        lines.append( '* Average precision %f \t recall %f\t F1 %f' %\
            (numpy.mean(precision), numpy.mean(recall), numpy.mean(f1)))
        print '\n'.join(lines)

    def get_summary(self):
        correct = 0

        precision = numpy.zeros(self.alphabet.size())
        recall = numpy.zeros(self.alphabet.size())
        f1 = numpy.zeros(self.alphabet.size())

        lines = []
        # computing precision, recall, and f1
        for i in xrange(self.alphabet.size()):
            precision[i] = self.matrix[i,i] / sum(self.matrix[i,:])
            recall[i] = self.matrix[i,i] / sum(self.matrix[:,i])
            if precision[i] + recall[i] != 0:
                f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            else:
                f1[i] = 0
            correct += self.matrix[i,i]
            label = self.alphabet.get_label(i)
            lines.append( '%s \tprecision %f \trecall %f\t F1 %f' %\
                    (label, precision[i], recall[i], f1[i]))
        lines.append( '* Overall accuracy rate = %f' %(correct / sum(sum(self.matrix[:,:]))))
        lines.append( '* Average precision %f \t recall %f\t F1 %f' %\
            (numpy.mean(precision), numpy.mean(recall), numpy.mean(f1)))
        return '\n'.join(lines)

    def get_average_prf(self):
        precision = numpy.zeros(self.alphabet.size())
        recall = numpy.zeros(self.alphabet.size())
        f1 = numpy.zeros(self.alphabet.size())

        lines = []
        # computing precision, recall, and f1
        for i in xrange(self.alphabet.size()):
            precision[i] = self.matrix[i,i] / sum(self.matrix[i,:])
            recall[i] = self.matrix[i,i] / sum(self.matrix[:,i])
            if precision[i] + recall[i] != 0:
                f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            else:
                f1[i] = 0
        return numpy.mean(precision), numpy.mean(recall), numpy.mean(f1)

    def get_accuracy(self):
        correct = 0

        precision = numpy.zeros(self.alphabet.size())
        recall = numpy.zeros(self.alphabet.size())
        f1 = numpy.zeros(self.alphabet.size())

        lines = []
        # computing precision, recall, and f1
        for i in xrange(self.alphabet.size()):
            precision[i] = self.matrix[i,i] / sum(self.matrix[i,:])
            recall[i] = self.matrix[i,i] / sum(self.matrix[:,i])
            if precision[i] + recall[i] != 0:
                f1[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])
            else:
                f1[i] = 0
            correct += self.matrix[i,i]
            label = self.alphabet.get_label(i)
            lines.append( '%s \tprecision %f \trecall %f\t F1 %f' %\
                    (label, precision[i], recall[i], f1[i]))

        return correct / sum(sum(self.matrix[:,:]))


    def print_out(self):
        """Printing out confusion matrix along with Macro-F1 score"""
        self.print_matrix()
        self.print_summary()


def matrix_to_string(matrix, header=None):
    """
    Return a pretty, aligned string representation of a nxm matrix.

    This representation can be used to print any tabular data, such as
    database results. It works by scanning the lengths of each element
    in each column, and determining the format string dynamically.

    the implementation is adapted from here
    mybravenewworld.wordpress.com/2010/09/19/print-tabular-data-nicely-using-python/

    Args:
        matrix - Matrix representation (list with n rows of m elements).
        header -  Optional tuple or list with header elements to be displayed.

    Returns:
        nicely formatted matrix string
    """

    if isinstance(header, list):
        header = tuple(header)
    lengths = []
    if header:
        lengths = [len(column) for column in header]

    #finding the max length of each column
    for row in matrix:
        for column in row:
            i = row.index(column)
            column = str(column)
            column_length = len(column)
            try:
                max_length = lengths[i]
                if column_length > max_length:
                    lengths[i] = column_length
            except IndexError:
                lengths.append(column_length)

    #use the lengths to derive a formatting string
    lengths = tuple(lengths)
    format_string = ""
    for length in lengths:
        format_string += "%-" + str(length) + "s "
    format_string += "\n"

    #applying formatting string to get matrix string
    matrix_str = ""
    if header:
        matrix_str += format_string % header
    for row in matrix:
        matrix_str += format_string % tuple(row)

    return matrix_str


class Alphabet(object):
    """Two way map for label and label index

    It is an essentially a code book for labels or features
    This class makes it convenient for us to use numpy.array
    instead of dictionary because it allows us to use index instead of
    label string. The implemention of classifiers uses label index space
    instead of label string space.
    """
    def __init__(self):
        self._index_to_label = {}
        self._label_to_index = {}
        self.num_labels = 0

    def __len__(self):
        return self.size()

    def __eq__(self, other):
        return self._index_to_label == other._index_to_label and \
            self._label_to_index == other._label_to_index and \
            self.num_labels == other.num_labels

    def size(self):
        return self.num_labels

    def has_label(self, label):
        return label in self._label_to_index

    def get_label(self, index):
        """Get label from index"""
        if index >= self.num_labels:
            raise KeyError("There are %d labels but the index is %d" % (self.num_labels, index))
        return self._index_to_label[index]

    def get_index(self, label):
        """Get index from label"""
        if not self.has_label(label):
            self.add(label)
        return self._label_to_index[label]

    def add(self, label):
        """Add an index for the label if it's a new label"""
        if label not in self._label_to_index:
            self._label_to_index[label] = self.num_labels
            self._index_to_label[self.num_labels] = label
            self.num_labels += 1

    def json_dumps(self):
        return json.dumps(self.to_dict())

    @classmethod
    def json_loads(cls, json_string):
        json_dict = json.loads(json_string)
        return Alphabet.from_dict(json_dict)

    def to_dict(self):
        return {
            '_label_to_index': self._label_to_index
            }

    @classmethod
    def from_dict(cls, alphabet_dictionary):
        """Create an Alphabet from dictionary

        alphabet_dictionary is a dictionary with only one field
        _label_to_index which is a map from label to index
        and should be created with to_dict method above.
        """
        alphabet = cls()
        alphabet._label_to_index = alphabet_dictionary['_label_to_index']
        alphabet._index_to_label = {}
        for label, index in alphabet._label_to_index.items():
            alphabet._index_to_label[index] = label
        # making sure that the dimension agrees
        assert(len(alphabet._index_to_label) == len(alphabet._label_to_index))
        alphabet.num_labels = len(alphabet._index_to_label)
        return alphabet


