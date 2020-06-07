# -*- coding: utf-8 -*-

"""
Created on 2020-06-06 19:00  

@author: congyingxu
"""



import kashgari
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari.corpus import ChineseDailyNerCorpus
from kashgari.tasks.labeling import BiLSTM_Model

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
    KashgariUsgaeInstance.train_x, KashgariUsgaeInstance.train_y = ChineseDailyNerCorpus.load_data('train')
    KashgariUsgaeInstance.valid_x, KashgariUsgaeInstance.valid_y = ChineseDailyNerCorpus.load_data('validate')
    KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y  = ChineseDailyNerCorpus.load_data('test')

    print(f"train data count: {len(KashgariUsgaeInstance.train_x)}")
    print(f"validate data count: {len(KashgariUsgaeInstance.valid_x)}")
    print(f"test data count: {len(KashgariUsgaeInstance.test_x)}")



def TrainBi_LSTM():
    print("----------tanining Bi_LSTM Model----------")
    model = BiLSTM_Model()
    model.fit(KashgariUsgaeInstance.train_x, KashgariUsgaeInstance.train_y, KashgariUsgaeInstance.valid_x, KashgariUsgaeInstance.valid_y)

    # Evaluate the model
    model.evaluate(KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y)
    # Model data will save to `saved_ner_model` folder
    model.save('saved_ner_model')
    print('TrainedModels/start to load')
    loaded_model = kashgari.utils.load_model('TrainedModels/saved_ner_model')
    res = loaded_model.predict(KashgariUsgaeInstance.test_x[:10])
    print(res)


def TrainBERTEmbedding():
    print("----------tanining BERT Model----------")
    bert_embed = BERTEmbedding('BERT/chinese_L-12_H-768_A-12/',task=kashgari.LABELING,sequence_length=100)
    # embedding = BERTEmbedding("bert-base-chinese", 200)

    model = BiLSTM_CRF_Model(bert_embed)
    model.fit(KashgariUsgaeInstance.train_x,
              KashgariUsgaeInstance.train_y,
              x_validate=KashgariUsgaeInstance.valid_x,
              y_validate=KashgariUsgaeInstance.valid_y,
              epochs=20,
              batch_size=512)

    # Evaluate the model
    model.evaluate(KashgariUsgaeInstance.test_x, KashgariUsgaeInstance.test_y)

    # Model data will save to  `saved_ner_model` folder
    model.save('TrainedModels/saved_ner_model_Chinese_BERT0607')

    loaded_model = kashgari.utils.load_model('TrainedModels/saved_ner_model_Chinese_BERT0607')
    res = loaded_model.predict(KashgariUsgaeInstance.test_x[:10])
    print(res)



if __name__ == '__main__':
    ImportCorpus()
    # TrainBi_LSTM()
    TrainBERTEmbedding()