#coding:utf-8
from util import singleton
import util, config, pickle

@singleton
class Non_Explicit_dict():
    def __init__(self):
        self.dict_word_pairs= self.get_dict_word_pairs()
        self.dict_production_rules= self.get_dict_production_rules()
        self.dict_dependency_rules= self.get_dict_dependency_rules()
        self.dict_Arg1_first = self.get_dict_Arg1_first()
        self.dict_Arg1_last = self.get_dict_Arg1_last()
        self.dict_Arg2_first = self.get_dict_Arg2_first()
        self.dict_Arg2_last = self.get_dict_Arg2_last()
        self.dict_Arg1_first_Arg2_first = self.get_dict_Arg1_first_Arg2_first()
        self.dict_Arg1_last_Arg2_last = self.get_dict_Arg1_last_Arg2_last()
        self.dict_Arg1_first3 = self.get_dict_Arg1_first3()
        self.dict_Arg2_first3 = self.get_dict_Arg2_first3()

        self.polarity, self.polarity_stem = self.get_polarity()
        self.negate, self.negate_stem = self.get_negate_word()

        self.dict_verb_classes = self.get_dict_verb_classes()

        self.brown_cluster = self.get_brown_cluster()

        self.dict_brown_cluster = self.get_dict_brown_cluster()

        self.inquirer, self.inquirer_stem = self.get_inquirer()

        # self.word2vec_dict = self.get_word2vec_dict()

        self.dict_main_verb_pair = util.load_dict_from_file(config.NON_EXPLICIT_DICT_MAIN_VERB_PAIR)

        self.cp_production_rules = util.load_dict_from_file(config.NON_EXPLICIT_DICT_CP_PRODUCTION_RULES)

        # cluster number
        self.word2vec_cluster = self.get_word2vec_cluster(5496)
        # word2vec_cluster pairs
        self.dict_word2vec_cluster_pairs = util.load_dict_from_file(config.NON_EXPLICIT_DICT_WORD2VEC_CLUSTER_PAIRS)

        # MPQA
        self.n_stemmed_word_pos_dict, self.y_stemmed_word_pos_dict = self.get_MAPA_polarity_dict()

        #tense
        self.dict_arg_tense_pair = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG_TENSE_PAIR)
        self.dict_arg1_tense = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG1_TENSE)
        self.dict_arg2_tense = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG2_TENSE)
        # first 3 conn
        self.dict_arg_first3_conn_pair = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG_FIRST3_CONN_PAIR)
        self.dict_arg1_first3_conn = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG1_FIRST3_CONN)
        self.dict_arg2_first3_conn = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG2_FIRST3_CONN)

        # verb pair
        self.dict_verb_pair = util.load_dict_from_file(config.NON_EXPLICIT_DICT_VERB_PAIR)

        # brown_cluster
        self.dict_Arg_brown_cluster = util.load_dict_from_file(config.NON_EXPLICIT_DICT_ARG_BROWN_CLUSTER)

        # context
        self.dict_prev_context_conn = util.load_dict_from_file(config.NON_EXPLICIT_DICT_PREV_CONTEXT_CONN)
        self.dict_prev_context_sense = util.load_dict_from_file(config.NON_EXPLICIT_DICT_PREV_CONTEXT_SENSE)
        self.dict_prev_context_conn_sense = util.load_dict_from_file(config.NON_EXPLICIT_DICT_PREV_CONTEXT_CONN_SENSE)

        self.dict_next_context_conn = util.load_dict_from_file(config.NON_EXPLICIT_DICT_NEXT_CONTEXT_CONN)

        self.dict_prev_next_context_conn = util.load_dict_from_file(config.NON_EXPLICIT_DICT_PREV_NEXT_CONTEXT_CONN)



        # print "non_explicit_dict is loaded..."



    def get_dict_word_pairs(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_WORD_PAIRS)

    def get_dict_production_rules(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_PRODUCTION_RULES)

    def get_dict_dependency_rules(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_DEPENDENCY_RULES)

    def get_dict_Arg1_first(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg1_first)

    def get_dict_Arg1_last(self):

        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg1_last)

    def get_dict_Arg2_first(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg2_first)

    def get_dict_Arg2_last(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg2_last)

    def get_dict_Arg1_first_Arg2_first(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg1_first_Arg2_first)

    def get_dict_Arg1_last_Arg2_last(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg1_last_Arg2_last)

    def get_dict_Arg1_first3(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg1_first3)

    def get_dict_Arg2_first3(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_Arg2_first3)

    def get_dict_brown_cluster(self):
        return util.load_dict_from_file(config.NON_EXPLICIT_DICT_BROWN_CLUSTER_PAIRS)

    def get_dict_verb_classes(self):
        dict = {}
        fin = open(config.LCSINFOMERGE_PATH)
        for line in fin:
            line = line.strip()
            word, veb_class = line.split(" ")
            dict[word] = veb_class
        fin.close()
        return dict

    def get_brown_cluster(self):
        dict = {}
        fin = open(config.BROWN_CLUSTER_PATH)
        for line in fin:
            c, w = line.strip().split("\t")
            dict[w] = c
        fin.close()
        return dict

    def get_word2vec_cluster(self, n_cluster):
        dict = {}
        fin = open(config.WORD2VEC_CLUSTER_PATH + str(n_cluster))
        for line in fin:
            c, w = line.strip().split("\t")
            dict[w] = c
        fin.close()
        return dict

    def get_inquirer(self):
        inquirer = {}
        inquirer_stem = {}
        fin = open(config.INQUIRER_WORD_PATH)
        for line in fin:
            key, value = line.strip().split("\t")
            inquirer[key] = value.split("|")
            inquirer_stem[util.stem_string(key)] = value.split("|")
        fin.close()
        return inquirer, inquirer_stem

    def get_negate_word(self):
        fin = open(config.NEGATE_WORDS_PATH)
        negate = []
        negate_stem = []
        for line in fin:
            word = line.strip()
            negate.append(word)
            negate_stem.append(util.stem_string(word))
        return negate, negate_stem

    def get_polarity(self):
        polarity = {}
        polarity_stem= {}
        for line in open(config.POLARITY_WORD_PATH):
            word, pol = line.strip().split("\t")
            polarity[word] = pol
            polarity_stem[util.stem_string(word)] = pol

        return polarity, polarity_stem


    def get_word2vec_dict(self):
        file = open(config.NON_EXPLICIT_DICT_WORD2VEC)
        dict_word2vec = {}
        for line in file:
            line = line.strip()
            word, string_vec = line.split(":")
            vec = [float(v) for v in string_vec.split(" ")]
            dict_word2vec[word] = vec
        return dict_word2vec

    # dict[(word, pos)] = (type, polarity)
    def get_MAPA_polarity_dict(self):
        n_stemmed_word_pos_dict = {}
        y_stemmed_word_pos_dict = {}

        fin = open(config.MPQA_SUBJECTIVITY_LEXICON_PATH)
        for line in fin:
            line = line.strip()
            if line == "":
                continue

            # if it has two polarities, choose the previous one
            _type, _, _word, _pos, _stemmed, _polarity = line.split(" ")[:6]

            type = _type.split("=")[-1]
            word = _word.split("=")[-1]
            pos = _pos.split("=")[-1]
            stemmed = _stemmed.split("=")[-1]
            polarity = _polarity.split("=")[-1]

            if stemmed == "n":
                n_stemmed_word_pos_dict[(word, pos)] = (type, polarity)
            if stemmed == "y":
                y_stemmed_word_pos_dict[(word, pos)] = (type, polarity)

        return n_stemmed_word_pos_dict, y_stemmed_word_pos_dict
