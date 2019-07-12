# -*- coding: utf-8 -*-

import pickle

#加载停用词词典
def get_stopwords():
    with open('data/stopword.txt', 'r',encoding='UTF-8') as f:
        stopword = [line.strip() for line in f]
    return set(stopword)


#传入切割后的词汇列表假如说是input_list[a,b,c,d]，n=3
#得到的结果[a,b,c,d][a,b,c][b,c,d][a,b][b,c][c,d]
def generate_ngram(input_list, n):
    result = []
    #list.extend在一个列表后面加入另一个列表中的所有值
    #i=1,2,3
    #当i=1时，j=0,[a,b,c,d]
    #当i=2时，j=0,1,[[a,b,c,d],[b,c,d]]------zip(*())-----[a,b][b,c][c,d]
    #当i=3时，j=0,1,2,[[a,b,c,d],[b,c,d],[c,d]]-----zip(*())-----[a,b,c][b,c,d]
    #以i=3,j=2为例，此时取得input_list[2:]=cd
    #zip(*[[a,b,c,d][b,c,d],[c,d]])按照最短的进行拼接得到[a,b,c][b,c,d]
    for i in range(1, n+1):
        #建立一个矩阵
        result.extend(zip(*[input_list[j:] for j in range(i)]))
    return result

#返回{单词：出现次数}词频大于2的
def load_dictionary(filename):
    """
    加载外部词频记录
    :param filename:
    :return:
    """
    word_freq = {}
    print('------> 加载外部词集')
    with open(filename, 'r',encoding='UTF-8') as f:
        for line in f:
            try:
                #按照行对文档进行切分，每一行去掉空格形成一个list
                line_list = line.strip().split(' ')
                # 规定最少词频
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = line_list[1]
            except IndexError as e:
                print(line)
                continue
    return word_freq


def save_model(model, filename):
    with open(filename, 'wb') as fw:
        pickle.dump(model, fw)


def load_model(filename):
    with open(filename, 'rb') as fr:
        model = pickle.load(fr)
    return model
