# -*- coding: utf-8 -*-

"""
Created on 2020-06-27 09:08  

@author: congyingxu

accauracy path
sklearn/metrics/classification.py
def accuracy_score(y_true, y_pred, normalize=True, sample_weight=None):
"""

import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)



import kashgari
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari import corpus

class KashgariUsgae:
    def __init__(self):
        self.train_x = []
        self.train_y = []
        self.valid_x = []
        self.valid_y = []
        self.test_x = []
        self.test_y = []


KashgariUsgaeInstance = KashgariUsgae()


dataset_folder = 'Dataset/ner_data/integrated_dataset/'
model_path = 'TrainedModels/saved_ner_model_Enghilsh_BERT0702_3_40epochs'

def ImportCorpus():
    #memc
    # KashgariUsgaeInstance.train_x, KashgariUsgaeInstance.train_y = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_train.txt')
    # KashgariUsgaeInstance.valid_x, KashgariUsgaeInstance.valid_y = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_valid.txt')
    # KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y  = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_test.txt')

    #all
    KashgariUsgaeInstance.train_x, KashgariUsgaeInstance.train_y = corpus.DataReader.read_conll_format_file(
        dataset_folder + 'all_train.txt')
    KashgariUsgaeInstance.valid_x, KashgariUsgaeInstance.valid_y = corpus.DataReader.read_conll_format_file(
        dataset_folder + 'all_valid.txt')
    KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y = corpus.DataReader.read_conll_format_file(
        dataset_folder + 'all_test.txt')

    print(f"train data count: {len(KashgariUsgaeInstance.train_x)}")
    print(f"validate data count: {len(KashgariUsgaeInstance.valid_x)}")
    print(f"test data count: {len(KashgariUsgaeInstance.test_x)}")


    # print(KashgariUsgaeInstance.train_x[:10], KashgariUsgaeInstance.train_y[:10])




def TrainBERTEmbedding():
    print("----------tanining BERT Model----------")
    bert_embed = BERTEmbedding('BERT/multilingual_L-12_H-768_A-12/',task=kashgari.LABELING,sequence_length=100)
    # embedding = BERTEmbedding("bert-base-chinese", 200)

    model = BiLSTM_CRF_Model(bert_embed)
    model.fit(KashgariUsgaeInstance.train_x,
              KashgariUsgaeInstance.train_y,
              x_validate=KashgariUsgaeInstance.valid_x,
              y_validate=KashgariUsgaeInstance.valid_y,
              epochs=40,
              batch_size=512)

    # Evaluate the model
    model.evaluate(KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y)

    # Model data will save to  `saved_ner_model` folder
    model.save(model_path)

    # loaded_model = kashgari.utils.load_model('TrainedModels/saved_ner_model_Enghilsh_BERT0629')
    # loaded_model.evaluate()
    # res = loaded_model.predict(KashgariUsgaeInstance.test_x[:100])
    # print(KashgariUsgaeInstance.test_x[:100])
    # print(res)


def EvaluateModel():
    test_dataset_folder = dataset_folder
    cate_list = ['memc','fileinc', 'httprs', 'dos', 'sqli', 'infor', 'gainpre', 'overflow', 'bypass', 'dirtra', 'csrf', 'xss', 'execution']
    loaded_model = kashgari.utils.load_model(model_path)

    for cate in cate_list:
        x_data, y_data = corpus.DataReader.read_conll_format_file( test_dataset_folder + cate +'_test.txt')
        print(len(x_data), cate, ' \n')
        loaded_model.evaluate(x_data, y_data)


def main():
    ImportCorpus()
    TrainBERTEmbedding()
    EvaluateModel()

if __name__ == '__main__':
    main()