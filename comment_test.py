# -*- coding: utf-8 -*-
from weibo import APIClient
import webbrowser
import pymysql,re,time

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改系统默认编码

APP_KEY = 'xxxxxxxx'#注意替换这里为自己申请的App信息
APP_SECRET = 'xxxxxxxxxxxxxx'#注意这里替换为自己申请的应用信息
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'#回调授权页面

#利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
print url
webbrowser.open_new(url)

#获取code=后面的内容
print '输入url中code后面的内容后按回车键：'
code = raw_input()
#code = your.web.framework.request.get('code')
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in

# 设置得到的access_token
client.set_access_token(access_token, expires_in)

comment_num = 1
i = 1

while True:
    r = client.comments.show.get(id = 4192500543207482,count = 200,page = i) #pgone 回应微博
    if len(r.comments):
        print '第 %s 页' % i
        for st in r.comments:
            print '第 %s 条评论' % comment_num
            created_at = st.created_at
            comment_id = st.id
            text = re.sub('回复.*?:','',str(st.text))
            source = re.sub('<.*?>|</a>','',str(st.source))
            user_name = st.user.screen_name
            followers = st.user.followers_count
            follow = st.user.friends_count
            province = st.user.province
            print created_at
            print comment_id
            print text
            print source
            print '评论者：%s,粉丝数：%s,关注数：%s,所在省份编号：%s' % (user_name,followers,follow,province)
            print '\n'


            conn = pymysql.connect(host='127.0.0.1',user='root',password='xxxx',charset='utf8',use_unicode=False)
            cur = conn.cursor()
            sql = "insert into weibo.test(created_at,comment_id,text,source,user_name,followers,follow,province) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            param = (created_at,comment_id,text,source,user_name,followers,follow,province)
            try:
                A = cur.execute(sql,param)
                conn.commit()
            except Exception,e:
                print(e)
                conn.rollback()
            comment_num+=1

        i+=1
        time.sleep(4)
    else:
        break
