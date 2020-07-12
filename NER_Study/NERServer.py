#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-----------------------------------------
@Author: congyingxu
@Created: 2020/07/12
------------------------------------------
@Modify: 2020/07/12
------------------------------------------
@Description:

NER server
"""

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import sys
import json,sqlite3
import kashgari
import nltk

sys.path.append('../')

# modify
loaded_ner_model = ''
trained_model_path = '/home/hadoop/dfs/data/Workspace/CongyingXU/CodeMiningTeam_Tasks/NER_Study/TrainedModels/saved_ner_model_Enghilsh_BERT0710_2_40epochs/'



class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data)
        print('post data from client:')
        print(post_data)

        result_data = {}

        opration = post_data['opration']
        if opration == 'NERFromRaw':
            input_message = post_data['input_message']
            result_data = NERFromRaw(input_message)

        self.send_response(200)
        self.end_headers()
        # self.wfile.write( bytes(str(result_data), encoding = "utf8" ))
        self.wfile.write( bytes(json.dumps( result_data ), encoding = "utf8"  ))


def init():
   global loaded_ner_model, trained_model_path
   loaded_ner_model = kashgari.utils.load_model(trained_model_path)
   print("Loading NER Model, Done!")

def NERFromRaw(input_massage):
    token_list = tokenize_word(input_massage)
    ner_result = NERFromTokenList(token_list)
    return ner_result


# 将输入内容 分句/词
def tokenize_word(message):
    sent_list = nltk.sent_tokenize(message)
    token_list = []
    for sent in sent_list:
        token_list.append(list( nltk.word_tokenize(sent)) )
    print(token_list)
    return token_list


def NERFromTokenList(input_token_list):
    ner_result = loaded_ner_model.predict(input_token_list)
    return ner_result


def StartServer():
    print('NER Server Started')
    sever = HTTPServer(("", 10088), PostHandler)
    sever.serve_forever()


if __name__ == '__main__':
    init()
    StartServer()
