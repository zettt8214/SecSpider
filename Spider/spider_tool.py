# -*- coding: utf-8 -*-
import random
from time import sleep
import requests
import pymysql
import datetime
from mail  import send_mail
import re
#请求头

headers = {}
headers[
    'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
headers['Connection'] = 'keep-alive'
headers['Upgrade-Insecure-Requests'] = '1'
agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
]

def get_page(url,proxies=None,sflag=1):
    t=3
    while t>0:
        try:
            headers['User-Agent']=random.choice(agents)
            if sflag:
                sleep(random.randint(1,3))
            print('正在下载：',url)
            print("date:",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
            s = requests.session()
            s.keep_alive = False  # 关闭多余连接
            if proxies:
                r = s.get(url,headers=headers,timeout=5,proxies=proxies)
            else:
                r = s.get(url, headers=headers, timeout=5)
        except Exception as r:
            print('errorinfo',r)
            sleep(2)
        else:
            if r.status_code==200:
                s.close()
                r.encoding=r.apparent_encoding
                #print('爬取成功！！！')
                return r.text
        t=t-1

# def db_conn():
#     try:
#         conn = sqlite3.connect('info.db')
#     except Exception as e:
#         print(e)
#     return conn


def conn():
    try:
        conn = pymysql.connect('localhost', 'root', 'root', 'secinfo')

    except Exception as e:
        print(e)
    return conn

def insert_info(title,time,href,source,content=''):
    co=conn()
    c=co.cursor()
    title=title.replace("'","''")
    if content:
        content=content.replace("'","''")
    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql="INSERT INTO info (title,content,time,href,source,date) values ("+"\'"+title+"\',"+"\'"+content+"\',"+"\'"+time+"\',"+"\'"+href+"\',"+"\'"+source+"\',"+"\'"+date+"\')"
    print(sql)
    try:
        c.execute(sql)
        a = re.search(r'dahua|hik|hikvision|uniview|camera|vulner|大华|海康|宇视|摄像头|',title, re.IGNORECASE)
        if a.group():
            send_mail(title,time,href,source,content)
    except Exception as e:
        print(e)
        pass
    co.commit()
    co.close()
