import shutil
import time

'''
备份词汇表
'''


def backup_vocab():
    '''
    '''
    t = round(time.time())
    shutil.copy2('vocab/vocab.pkl', 'backup/vocab_' + str(t) + '.pkl')
    shutil.copy2('vocab/vocab.txt', 'backup/vocab_' + str(t) + '.txt')
    return True

if __name__ == '__main__':
    backup_vocab()
