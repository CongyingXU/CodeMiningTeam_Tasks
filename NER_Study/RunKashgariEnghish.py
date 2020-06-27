# -*- coding: utf-8 -*-

"""
Created on 2020-06-27 09:08  

@author: congyingxu
"""




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


def ImportCorpus():
    KashgariUsgaeInstance.train_x, KashgariUsgaeInstance.train_y = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_train.txt')
    KashgariUsgaeInstance.valid_x, KashgariUsgaeInstance.valid_y = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_valid.txt')
    KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y  = corpus.DataReader.read_conll_format_file('Dataset/ner_data/memc_test.txt')

    print(f"train data count: {len(KashgariUsgaeInstance.train_x)}")
    print(f"validate data count: {len(KashgariUsgaeInstance.valid_x)}")
    print(f"test data count: {len(KashgariUsgaeInstance.test_x)}")

    print(KashgariUsgaeInstance.train_x[:10], KashgariUsgaeInstance.train_y[:10])




def TrainBERTEmbedding():
    print("----------tanining BERT Model----------")
    bert_embed = BERTEmbedding('BERT/multilingual_L-12_H-768_A-12/',task=kashgari.LABELING,sequence_length=100)
    # embedding = BERTEmbedding("bert-base-chinese", 200)

    model = BiLSTM_CRF_Model(bert_embed)
    model.fit(KashgariUsgaeInstance.train_x,
              KashgariUsgaeInstance.train_y,
              x_validate=KashgariUsgaeInstance.valid_x,
              y_validate=KashgariUsgaeInstance.valid_y,
              epochs=10,
              batch_size=512)

    # Evaluate the model
    model.evaluate(KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y)

    # Model data will save to  `saved_ner_model` folder
    model.save('TrainedModels/saved_ner_model_Enghilsh_BERT0627')

    loaded_model = kashgari.utils.load_model('TrainedModels/saved_ner_model_Enghilsh_BERT0627')
    res = loaded_model.predict(KashgariUsgaeInstance.test_x[:100])
    print(KashgariUsgaeInstance.test_x[:100])
    print(res)



if __name__ == '__main__':
    ImportCorpus()
    TrainBERTEmbedding()