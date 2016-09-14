# -*- coding: utf-8 -*-
import pickle
from collections import defaultdict

'''
初始化词汇表
'''

ddict = defaultdict(int) # 这里传入int，当ddict['key']这个key不存在时，默认返回0
ddict['hello'] = 10
ddict['world'] = 10
ddict['girl'] = 10

def save_vocab(vocab):
    with open('vocab/vocab.pkl', 'wb') as fpk:
        pickle.dump(vocab, fpk)
    with open('vocab/vocab.txt', 'w', encoding='utf8') as f:
        for item in sorted(vocab.items()):
            print(item, file=f)
    return True

if __name__ == '__main__':
    save_vocab(ddict)
    print(ddict)
    ddict['albeit'] += 1
    print(ddict)
