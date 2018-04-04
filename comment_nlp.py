# -*- coding: utf-8 -*-

import pymysql,re
import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud,ImageColorGenerator
from collections import Counter

def readmysql():
    commentlist = []
    textlist = []
    userlist = []
    conn = pymysql.connect(host='127.0.0.1', user='root', password='xxxx',charset='utf8')
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM weibo.response WHERE id < '%d'" % 10000)
        rows = cur.fetchall()
        for row in rows:
            row = list(row)
            del row[0]
            if row not in commentlist:
                commentlist.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                comment_id = row[0]
                user_name = row[1]
                userlist.append(user_name)
                created_at = row[2]
                text = row[3]
                if text:
                    textlist.append(text)
                like_num = row[4]
                source = row[5]

    return commentlist,userlist,textlist

def word2cloud(textlist):
    fulltext = ''
    isCN = 1
    back_coloring = imread("123.jpg")
    cloud = WordCloud(font_path='font.ttf',
                      background_color="white",
                      max_words=2000,
                      mask=back_coloring,
                      max_font_size=100,
                      random_state=42,
                      width=1000,height=860,margin=2)

    for li in textlist:
        fulltext += ' '.join(jieba.cut(li,cut_all =False))
    wc = cloud.generate(fulltext)
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('评论词云.png')

def snowanlaysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)

        sentimentslist.append(s.sentiments)

    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist,bins=np.arange(0,1,0.02))
    plt.show()

def emojilist(textlist):
    emojilist = []
    for li in textlist:
        emojis = re.findall(re.compile(u'(\[.*?\])',re.S),li)
        if emojis:
            for emoji in emojis:
                emojilist.append(emoji)
    emojidict = Counter(emojilist)
    print(emojidict)
    
def follows(textlist):
    userdict = Counter(userlist)
    print(userdict.most_common(20))

if __name__ == '__main__':
    commentlist,userlist,textlist = readmysql()
    word2cloud(textlist)
    snowanlaysis(textlist)
    emojilist(textlist)
    follows(textlist)




