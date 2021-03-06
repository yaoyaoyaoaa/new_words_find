# -*- coding: utf-8 -*-

import os
import jieba
from model import TrieNode
from utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from config import basedir

#打开数据文件去掉停用词利用结巴进行粗略的分词处理
def load_data(filename, stopwords):
    """

    :param filename:
    :param stopwords:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, 'r',encoding='UTF-8') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            data.append(word_list)
    return data


def load_data_2_root(data):
    #传入经过粗略分词
    print('------> 插入节点')
    #对于每一行句子进行n-gram的组合
    for word_list in data:
        # tmp 表示每一行自由组合后的结果（n gram）
        # tmp: [['它'], ['是'], ['小'], ['狗'], ['它', '是'], ['是', '小'], ['小', '狗'], ['它', '是', '小'], ['是', '小', '狗']]
        ngrams = generate_ngram(word_list, 3)
        #建立存储这些词汇的字典树，存储词汇出现的次数
        for d in ngrams:
            root.add(d)
    print('------> 插入成功')


if __name__ == "__main__":
    #root_name = basedir + "/data/root.pkl"
    root_name = basedir + "/data/jianzhu.pkl"
    stopwords = get_stopwords()
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        #文档不能正确反映单个词的词频，所以引入Jieba自带的外部词典
        dict_name = basedir + '/data/dict.txt'
        #读取字典文件，取出词频大于2的建立字典{单词：频数}
        word_freq = load_dictionary(dict_name)
        #建立词汇树
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    # 加载新的文章
    #filename = 'data/demo.txt'
    filename = 'data/jianzhu.txt'
    #data是二维数组，存储[[第一行list][第二行list].....]
    data = load_data(filename, stopwords)
    # 将新的文章插入到Root中
    load_data_2_root(data)

    # 定义取TOP5个
    topN = 5
    result, add_word = root.find_word(topN)
    # 如果想要调试和选择其他的阈值，可以print result来调整
    # print("\n----\n", result)
    print("\n----\n", '增加了 %d 个新词, 词语和得分分别为: \n' % len(add_word))
    print('#############################')
    for word, score in add_word.items():
        print(word + ' ---->  ', score)
    print('#############################')

    # 前后效果对比
    #test_sentence = '蔡英文在昨天应民进党当局的邀请，准备和陈时中一道前往世界卫生大会，和谈有关九二共识问题'
    test_sentence = '在分配电箱设置插座直接给末级配电箱供电'
    print('添加前：')
    print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))

    for word in add_word.keys():
        jieba.add_word(word)
    print("添加后：")
    print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))
