# -*- coding: utf-8 -*-
from weibo import APIClient
import webbrowser        #python内置的包

APP_KEY = 'xxxxxxx'#注意替换这里为自己申请的App信息
APP_SECRET = 'xxxxxxxxxxxxxxxx'#注意替换这里为自己申请的应用密钥
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

#可以打印下看看里面都有什么东西
statuses = client.statuses__friends_timeline()['statuses'] #获取当前登录用户以及所关注用户（已授权）的微博</span>

length = len(statuses)
print length
#输出了部分信息
for i in range(0,length):
    print u'昵称：'+statuses[i]['user']['screen_name']
    print u'简介：'+statuses[i]['user']['description']
    print u'位置：'+statuses[i]['user']['location']
    print u'微博：'+statuses[i]['text']