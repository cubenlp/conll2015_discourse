#coding:utf-8
import os, config
import mallet_util
import pickle


class Strategy:
    def train_model(self, train_file_path, model_path):
        return None
    def test_model(self, test_file_path, result_file_path, model_path):
        return None


''' MaxEnt '''
class MaxEnt(Strategy):
    def __init__(self):
        self.trainer = "MaxEnt"

    def train_model(self, train_file_path, model_path):
        print "training %s ..." % (self.trainer)


        cmd = config.MALLET_PATH + \
              "/bin/mallet import-svmlight --input " + train_file_path + " --output "+ config.MALLET_FILE
        os.system(cmd)
        cmd = config.MALLET_PATH + \
              "/bin/mallet train-classifier --input " + config.MALLET_FILE + \
              " --output-classifier " + model_path + " --trainer " + self.trainer \
              # + " -Xms256m -Xmx2048m "
              # + " --cross-validation 10"
        os.system(cmd)
        print "\n%s model 已经生成：%s " %( self.trainer, model_path)

    def test_model(self, test_file_path, result_file_path, model_path):
        cmd = config.MALLET_PATH + "/bin/mallet classify-file --input " + test_file_path + " --output " + result_file_path + " --classifier " + model_path
        os.system(cmd)
        print "test the model ..."



''' Naive Bayes '''
class NaiveBayes(Strategy):
    def __init__(self):
        self.trainer = "NaiveBayes"

    def train_model(self, train_file_path, model_path):
        print "training %s ..." % (self.trainer)

        cmd = config.MALLET_PATH + \
              "/bin/mallet import-svmlight --input " + train_file_path + " --output "+ config.MALLET_FILE
        os.system(cmd)
        cmd = config.MALLET_PATH + \
              "/bin/mallet train-classifier --input " + config.MALLET_FILE + \
              " --output-classifier " + model_path + " --trainer " + self.trainer \
              # + " --cross-validation 10"
        os.system(cmd)
        print "\n %s model 已经生成：%s " %(self.trainer, model_path)

    def test_model(self, test_file_path, result_file_path, model_path):
        cmd = config.MALLET_PATH + "/bin/mallet classify-file --input " + test_file_path + " --output " + result_file_path + " --classifier " + model_path
        os.system(cmd)
        print "test the model ..."


class Mallet_classifier:
    def __init__(self,strategy):
        self.strategy = strategy

    def train_model(self, train_file_path, model_path):
        self.strategy.train_model(train_file_path, model_path)

    def test_model(self, test_file_path, result_file_path, model_path):
        self.strategy.test_model(test_file_path, result_file_path, model_path)


if __name__ == "__main__":
    pass
