# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:41:22 2019

@author: Onedas
"""

import json
import requests
from flask import Flask, request, Response
import intent_finder as IF

# %%
#%%global variables
API_KEY = 'API_KEY'

#%% URL
SEND_MESSAGE_URL = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
SEND_IMAGE_URL = 'https://api.telegram.org/bot{token}/sendPhoto'.format(token=API_KEY)

# %% data load and train # intent_finder
intent_finder = IF.Intent_Finder()
DB_file = 'dasan120_FAQ2.xlsx'
df = pd.read_excel(DB_file)
for i in range(len(df)):
    intent_finder.train(df.loc[i][1], df.loc[i][2], i) 
print('Load data : Done')
# %% function of backend
def text2Qnums(text):
    return intent_finder.find_answer(text)

def Qnum2Q(Qnum):
    s=''
    s+='[{}]Q{} : '.format(df.loc[Qnum][1],Qnum)+ df.loc[Qnum][2]
    
    return s        

def Qnum2A(Qnum):
    s=''
    s+='A : '+ df.loc[Qnum][3]
    return s

#print(Qnum2Q(282))
#print(Qnum2A(284))
#print(intent_finder.find_answer('주정차 위반'))
#print(text2Qnums('주정차 위반'))
# %% function of telegram
app = Flask(__name__)

def parse_message(data):
    '''응답data 로부터 chat_id 와 text, user_name을 추출.'''
    chat_id = None
    msg = None
    user_name = None
    inline_data = None    
    
    if 'callback_query' in data:
        data=data['callback_query']
        inline_data = data['data']
        
    chat_id = data['message']['chat']['id']
    msg = data['message']['text']
    user_name = data['message']['chat']['first_name'] + data['message']['chat']['last_name']

    return chat_id, msg, user_name, inline_data    #https://core.telegram.org/bots/api#keyboardbutton


def send_message(chat_id, text):
    params = {'chat_id':chat_id, 'text': text}
    requests.post(SEND_MESSAGE_URL, json=params)

def send_message_keyboard(chat_id, text):
    keyboard = {'keyboard' : [[{'text': 'A'},{'text': 'B'}],
                              [{'text': 'C'},{'text': 'D'}]],
                'one_time_keyboard':True}
    
    params = {'chat_id':chat_id, 'text' : text, 'reply_markup':keyboard}
    requests.post(SEND_MESSAGE_URL, json=params)

def send_message_inlinekeyboard(chat_id,text,page=0):
    answer_nums = text2Qnums(text)
    print('answer num : ',answer_nums)
    text1 = Qnum2Q(answer_nums[0])
    text2 = Qnum2Q(answer_nums[1])
    text3 = Qnum2Q(answer_nums[2])
    InlineKeyboard = {'inline_keyboard' : [[{'text':text1, 'callback_data':answer_nums[0]}],
                                           [{'text':text2, 'callback_data':answer_nums[1]}],
                                           [{'text':text3, 'callback_data':answer_nums[2]}]]}

    params = {'chat_id':chat_id, 'text' : '{}에 대해 가장 유사도가 높은 답변 입니다'.format(text), 'reply_markup':InlineKeyboard}
    requests.post(SEND_MESSAGE_URL,json=params)
    

# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        message = request.get_json()
        with open('message.txt','w') as f:
            json.dump(message,f,indent=4)
        
        
        chat_id, msg, chat_name, inline_data = parse_message(message)
        print(inline_data)
        if inline_data == None:
            send_message_inlinekeyboard(chat_id,msg)
        else:
            send_message(chat_id,Qnum2A(int(inline_data)))
            inline_data =None
            
        # print(inline_data)
#            send_message_inlinekeyboard(chat_id,msg)
#            send_message_keyboard(chat_id, msg)
#            send_message(chat_id,msg)
        
#        except:
#            print('실행 안됨')
#        
        return Response('ok', status=200)
        
    else:
        return 'Hello World!'


if __name__ == '__main__':
    app.run(port = 5000)
