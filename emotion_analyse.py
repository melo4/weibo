# -*- coding: utf-8 -*-
import jieba
import numpy as np

def open_dict(Dict = 'open',path = r'/Users/mengxiao/PycharmProjects/emotion/'):
    path = path + '%s.txt' % Dict
    dictionary = open(path,'r',encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict  #返回列表

def judge(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'

deny_word = open_dict(Dict = '否定词',path = r'/Users/mengxiao/Textming/')
posdict = open_dict(Dict = 'positive',path = r'/Users/mengxiao/Textming/')
negdict = open_dict(Dict = 'negative',path = r'/Users/mengxiao/Textming/')
degree_word = open_dict(Dict= '程度级别词语',path = r'/Users/mengxiao/Textming/')

# 权重由高到低，
mostdict = degree_word[degree_word.index('extreme')+1 : degree_word.index('very')]
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')]
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('last')]

def sentiment_score_list(dataset):
    seg_sentence = dataset.split('。')

    count1 = []
    count2 = []
    for sen in seg_sentence:
        segtmp = jieba.lcut(sen, cut_all=False) # 对句子进行分词，并以列表形式返回。
        i = 0 # 记录扫描到词的位置
        j = 0 # 记录情感词的位置
        poscount = 0 # 积极词的第一次分值
        poscount2 = 0 # 积极词反转后的分值
        poscount3 = 0 # 积极词的最终分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0

        for word in segtmp:
            if word in posdict: # 判断词语是否是情感词
                poscount += 1
                c = 0 # 否定词个数
                for w in segtmp[j:i]:
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judge(c) == 'odd':
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                j = i + 1  # 情感词位置变化

            elif word in negdict:
                negcount += 1
                d = 0
                for w in segtmp[j:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in deny_word:
                        d += 1
                if judge(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                j = i + 1  # 情感词位置变化
            elif word == '！' or word == '!': # 判断句子是否有感叹号
                for w2 in segtmp[::-1]:
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1 # 扫描词位置前移


            # 以下是防止出现负数的情况

            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return count2

def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        score.append([Pos,Neg])
    return score


data1 = '你就是个王八蛋，混账玩意！你们的手机真不好用！我非常生气！！！！'
data2 = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心！'

print (sentiment_score(sentiment_score_list(data1)))
print (sentiment_score(sentiment_score_list(data2)))





