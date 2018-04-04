# -*- coding: utf-8 -*-
import pymysql,re,time,requests

#Pgone回应微博ID：4192500543207482

weibo_id = 4192500543207482   # input('输入单条微博ID：')
# url='https://m.weibo.cn/single/rcList?format=cards&id=4192500543207482&type=comment&hot=1&page={}' #爬热门评论
url='https://m.weibo.cn/api/comments/show?id=4192500543207482&page={}' #爬时间排序评论
headers = {
    'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Host' : 'm.weibo.cn',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Referer' : 'https://m.weibo.cn/status/4192500543207482',
    'Cookie' : 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W50ic.eDLvgYsrQXyffhbay5JpX5K-hUgL.FoeN1hMNe0e7eo-2dJLoI7_SdgHV9NyDqgvae5tt;SUHB=02MvZbDGrK2xQh;SUB=_2A253vYJuDeRhGeVJ41UW8y3MyTmIHXVVQS4mrDV6PUJbktBeLRnNkW1NT8Uxylr_X7ihbRPAsGoHvyMe-m1VDguR;SCF=AjbvCvnn6cFfvStw42Unvmy0fnmfrzDjUEgoGOutGhzsTXeUK1Ozd-6flNTG4uPUSUGT4tD-yuLOa9uyDQGhko0.;M_WEIBOCN_PARAMS=uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword;H5_INDEX_TITLE=Mmengxiaoo0;H5_INDEX=0_all;ALF=1524726828;_T_WM=136847b9a3ccf2b122897afe9e7d254e',
    'DNT' : '1',
    'Connection' : 'keep-alive',
    }
i = 120
comment_num = 1
while True:
    # if i==1:     # 爬热门评论
    #     r = requests.get(url = url.format(i),headers = headers)
    #     comment_page = r.json()[1]['card_group']
    # else:
    #     r = requests.get(url = url.format(i),headers = headers)
    #     comment_page = r.json()[0]['card_group']
    r = requests.get(url=url.format(i), headers=headers)  #  爬时间排序评论
    try:
        comment_page = r.json()['data']['data']
    except Exception as e:
        print (e.args)
        print (r)
        print (r.text)



    if r.status_code == 200:
        try:
            print('正在读取第 %s 页评论：' % i)
            for j in range(0,len(comment_page)):
                print('第 %s 条评论' % comment_num)
                user = comment_page[j]
                print(user)
                comment_id = user['user']['id']
                print(comment_id)
                user_name = user['user']['screen_name']
                print(user_name)
                created_at = user['created_at']
                print(created_at)
                text = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '', user['text'])
                print(text)
                like_num = user['like_counts']
                print(like_num)
                source = re.sub('[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '', user['source'])
                print(source + '\r\n')
                conn = pymysql.connect(host='127.0.0.1', user='root', password='xxxxx', charset='utf8', use_unicode=False)
                cur = conn.cursor()
                sql = "insert into weibo.response(comment_id,user_name,created_at,text,like_num,source) values(%s,%s,%s,%s,%s,%s)"
                param = (comment_id,user_name,created_at,text,like_num,source)
                try:
                    A = cur.execute(sql, param)
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()
                comment_num+=1

            i+=1
            time.sleep(0.2)
        except:
            i+1
            pass
    else:
        break