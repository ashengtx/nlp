import nltk
import pickle
import re
import numpy as np
from collections import defaultdict

from init import save_vocab
from backup import backup_vocab


LETTER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
    text = re.sub(r'[_=\.]', ' ', text)
    words = [word.lower() for word in nltk.word_tokenize(text) if len(word) > 1]
    ret = []
    for word in words:
        if word[0] not in LETTER:
            continue
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
        print('是否所有的new_words都是生词？(y/n)')
        op = input("word_app/recognize/veirfy>")
        # 如果输入y和n以外的命令，则循环
        while (op != 'y' and op !='n'):
            print('是否所有的new_words都是生词？(请输入y或者n)(y/n)')
            op = input("word_app/recognize/veirfy>")
        if op == 'n':
            input_str = input("请输入已掌握的单词，用空格隔开：")
            input_words = input_str.split()
            # 如果输入的词不在new_words里面，则再次输入
            flag = False
            wrong_word = []
            for w in input_words:
                if w not in new_words:
                    wrong_word.append(w)
                    flag = True
            if flag:
                print('你输入了未出现的单词: ')
                print(wrong_word)
            else:
                for w in input_words:
                    new_words.remove(w)
                    mastered.append(w)
        if op == 'y':
            break
    return (new_words, mastered)

def welcome():
    '''
    menu
    '''
    welcome_message = '''
    欢迎使用生词识别app！！！
    '''
    menu = '''
    输入以下命令执行相应功能：
    v/vocab         显示已掌握及待掌握的单词
    r/recognize     开始生词识别
    q/quit          退出
    '''
    print(welcome_message)
    while True:
        print(menu)
        op = input('word_app>')
        if op in ['q', 'quit']:
            print('\n你会想念我的！')
            quit()
        elif op in ['r', 'recognize']:
            recognize()
        elif op in ['v', 'vocab']:
            vocab()
        else:
            print('请输入正确的命令')
    return True

def recognize():
    '''
    生词识别
    '''
    # 获得文章里的单词
    print('请输入article目录下的英文文章名字，m或menu返回主菜单，q或quit退出')
    filename = input('word_app/recognize>')
    if filename in ['q', 'quit']:
        quit()
    elif filename in ['m', 'menu']:
        welcome()
    else :
        # 这里需要一个异常处理，文件不存在的情况
        words = get_words_from_txt('article/'+filename)
    
    # 获得个人词汇表
    # 词汇表是一个dict，key是单词，value是掌握程度
    # 0为掌握，其他为见过次数
    vocab = get_vocab('vocab/vocab.pkl')
    
    # 显示已掌握的词
    mastered = [w for w in vocab if vocab[w] >= 10]

    # 获得未掌握的单词，即value<10，
    new_words = get_new_words(words, mastered)

    # 让用户确认这些单词是否都是未掌握的
    new_words, mastered = verification(new_words)

    # 更新vocab
    for w in new_words:
        vocab[w] += 1
    for w in mastered:
        vocab[w] = 10

    print('在这篇文章里你一共遇到了{}个生词:'.format(len(new_words)))
    print(new_words)
    print('你的词汇表又增加了{}个已掌握的单词:'.format(len(mastered)))
    print(mastered)
    
    master_num = 0
    unmaster_num = 0
    for w in vocab:
        if vocab[w] >= 10:
            master_num += 1
        else:
            unmaster_num += 1
    print('你的词汇表当前一共有{0}个单词，其中已掌握{1}个，还有{2}个待掌握。'.format(len(vocab), master_num, unmaster_num))

    # 保存vocab
    if save_vocab(vocab):
        print('词汇表已保存')

    # 备份vocab
    if backup_vocab():
        print('词汇表已备份')

def vocab():
    vocab = get_vocab('vocab/vocab.pkl')
    mastered = []
    unmastered = []
    for w in vocab:
        if vocab[w] >= 10:
            mastered.append((w, vocab[w]))
        else:
            unmastered.append((w, vocab[w]))

    print('你的词汇表当前一共有{0}个单词，其中已掌握{1}个，还有{2}个待掌握。'.format(len(vocab), len(mastered), len(unmastered)))
    message = '''
    s/show          显示词汇表
    m/menu          返回主菜单
    r/recognize     开始生词识别
    '''
    print(message)
    op = input('word_app/vocab>')
    while True:
        if op in ['m', 'menu']:
            return True
        elif op in ['r', 'recognize']:
            recognize()
            return True
        elif op in ['s', 'show']:
            print('mastered: ')
            print(mastered)
            print('unmastered: ')
            print(unmastered)
            return True
        else:
            print('请输入正确的命令！')
            print(message)
            op = input('word_app/vocab>')
    return True

if __name__ == '__main__':

    welcome()
    
