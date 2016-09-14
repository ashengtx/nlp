import nltk
import pickle
import re
import numpy as np
from collections import defaultdict

from init import save_vocab
from backup import backup_vocab


INPUT_TEXT = ''

def get_vocab(filename):
    with open(filename, 'rb') as fpk:
        return pickle.load(fpk)

def fuck(filename):
    print('fuck ', filename)
    return

def get_words_from_txt(filename):
    with open(filename, 'r', encoding='utf8') as fl:
        text = fl.read()
    words = [word.lower() for word in nltk.word_tokenize(text) if len(word) > 1]
    ret = []
    for word in words:
        # 去掉所有格 ’s ’d等
        if re.match(r'.*’\w{1,2}$', word):
            ret.append(word[0:-2])
        else:
            ret.append(word)
    return sorted(set(ret))

def get_new_words(words, mastered):
    return [word for word in words if word not in mastered]

def verification(words):
    mastered = []
    new_words = words
    op = ''
    # 输入0000表示确认完毕
    while op != '0000':
        print('new_words: ')
        print(new_words)
        print('mastered: ')
        print(mastered)
        op = input("是否所有的new_words都是生词？(y/n)")
        # 如果输入y和n以外的命令，则循环
        while (op != 'y' and op !='n'):
            op = input("是否所有的new_words都是生词？(请输入y或者n)(y/n)")
        if op == 'n':
            input_str = input("请输入已掌握的单词，用空格隔开：")
            input_words = input_str.split()
            # 如果输入的词不在new_words里面，则再次输入
            flag = False
            for w in input_words:
                if w not in new_words:
                    flag = True
            if flag:
                print('你输入了未出现的单词')
            else:
                for w in input_words:
                    new_words.remove(w)
                    mastered.append(w)
        if op == 'y':
            break
    return (new_words, mastered)


if __name__ == '__main__':
    # 获得文章里的单词
    filename = input('请输入你看过的英文文章名字，确保是txt文件，并且位于article目录下: ')
    
    words = get_words_from_txt('article/'+filename)
    #print('words: ', words)
    
    # 获得个人词汇表
    # 词汇表是一个dict，key是单词，value是掌握程度
    # 0为掌握，其他为见过次数
    vocab = get_vocab('vocab/vocab.pkl')
    #fuck('vocab/my_vocab.txt')
    #print('vacab: ', vocab)
    
    # 显示已掌握的词
    mastered = [w for w in vocab if vocab[w] >= 10]
    #print('mastered: ', mastered)

    # 获得未掌握的单词，即value<10，
    new_words = get_new_words(words, mastered)
    #print('new_words: ', new_words)

    # 让用户确认这些单词是否都是未掌握的
    new_words, mastered = verification(new_words)
    print('new_words: ')
    print(new_words)
    print('mastered: ')
    print(mastered)
    
    # 更新vocab
    print('before update')
    print(vocab)
    for w in new_words:
        vocab[w] += 1
    for w in mastered:
        vocab[w] = 10
    print('after update')
    print(vocab)
    
    quit()
    # 保存vocab
    if save_vocab(vocab):
        print('词汇表已保存')

    # 备份vocab
    if backup_vocab():
        print('词汇表已备份')
