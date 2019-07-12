with open('data/test.txt', 'r', encoding='UTF-8') as f:
    word_freq = {}
    for line in f:

            # 按照行进行切分，对于每一行按照空格切分，将所有的文档中的单词形成一个List
        line_list = line.strip().split(' ')
        #print(line_list[1])
        print(line_list)


