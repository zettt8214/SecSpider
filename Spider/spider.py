#!/usr/bin/python
# -*- coding: UTF-8 -*-


from bs4 import BeautifulSoup
from spider_tool import get_page,insert_info
from mail import send_mail
import re
import requests
import sys
import pymysql
import datetime

proxies = { "http": "http//127.0.0.1:1080", }


def search_anquanke(flag=1):

    url='https://www.anquanke.com/'
    html=get_page(url,sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titles=soup.find_all(class_='title')
        content= soup.find_all(class_='desc hide-in-mobile-device')
        time = soup.find_all(class_='date')
        title_lst=[]
        href_lst=[]
        content_lst=[]
        time_lst=[]
        for tag in titles:
            if tag.a:
                title_lst.append(tag.a.string)
                href_lst.append(url+tag.a['href'][1:])
        for tag in content:
            content_lst.append(tag.string)
        for tag in time:
            time_lst.append(tag.span.text.strip())
        for i in range(0, len(href_lst)):
           insert_info(title=title_lst[i], content=content_lst[i], time=time_lst[i], href=href_lst[i],source='anquanke')
    except Exception as e:
        print(e)


def func(tag):
    return  tag.has_attr('data-datetime')

def search_ipvm(flag=1):
    url='https://ipvm.com/'
    html=get_page(url,sflag=flag)
    try:
        soup=BeautifulSoup(html,'html.parser')
        titles=soup.find_all(class_='title-link-primary')
        time=soup.find_all(func)
        content=soup.find_all(class_='article-snippet text-muted m-b-0 hidden-xs-down')
        content1=soup.find_all(class_='article-snippet text-muted hidden-sm-down')
        #print(desc1)
        time_lst = []
        href_lst = []
        title_lst = []
        content_lst = []
        content_lst.append(content1[0].string)
        for tag in titles:
            title_lst.append(tag.string)
            href_lst.append(tag['href'])
        for tag in time:
            time_lst.append(tag['data-datetime'])
        for tag in content:
            content_lst.append(tag.string)

        for i in range(0,len(href_lst)):
            insert_info(title=title_lst[i],content=content_lst[i],time=time_lst[i],href=href_lst[i],source="ipvm")
    except Exception as a:
        print(a)

def hik(flag=1):
    url='http://www.hikvision.com/cn/support_list_591.html'
    html=get_page(url,sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags=soup.select('li[class="clearfix"]')
        titles=[]
        hrefs=[]
        time=[]
        for tag in tags:
            titles.append(tag.a.string)
            hrefs.append('http://www.hikvision.com/cn/'+tag.a['href'])
            time.append(tag.span.string)
        for i in range(0,len(titles)):
            insert_info(title=titles[i],time=time[i],href=hrefs[i],source="hik")
    except Exception as a:
        print(a)

def yushi(flag=1):
    url='http://cn.uniview.com/Security/Notice/'
    html=get_page(url,sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('ul[id="NewsListStyle"]')
        href_lst=[]
        title_lst=[]
        time_lst=[]
        for tag in (tags[0].find_all('a')):
            href_lst.append('http://cn.uniview.com'+tag['href'])
            title_lst.append(tag.string)
            date=tag['href'].split('/')[3][:4]+'-'+tag['href'].split('/')[3][-2:]
            time_lst.append(date)
        for i in range(0,len(title_lst)):
            insert_info(title=title_lst[i],time=time_lst[i],href=href_lst[i],source='uniview')
    except Exception as a:
        print(a)

def cert(flag=1):
    url="http://cert.360.cn"
    html = get_page(url, sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titles=soup.find_all(class_='news-title')
        date=soup.find_all(class_='news-date')
        content=soup.find_all(class_="news-conent")

        title_lst=[]
        href_lst=[]
        time_lst=[]
        content_lst=[]
        for tag in titles:
            title_lst.append(tag.a.string)
            href_lst.append(url+tag.a['href'])

        for tag in date:
            time_lst.append(tag.string.split(' ')[1].strip())

        for tag in content:
            content_lst.append(tag.string)

        for i in range(len(title_lst)):

            insert_info(title=title_lst[i],content=content_lst[i],time=time_lst[i],href=href_lst[i],source='360cert')
    except Exception as a:
        pass

def eanqun(flag=1):
    url="https://www.easyaq.com/daily"
    html=get_page(url,sflag=flag)

    try:
        soup=BeautifulSoup(html, 'html.parser')
        titles=soup.find_all('h3')
        content=soup.find_all('p')
        date=soup.select('div[class="source"] > span > span')
        href_lst=[]
        content_lst=[]
        title_lst=[]
        date_lst=[]
        if titles:
            for tag in titles:
                title_lst.append(tag.a.string)
                href_lst.append("https://www.easyaq.com"+tag.a['href'])
        if content:
            for tag in content:
                content_lst.append(tag.string)
        if date:
            for tag in date:
                date_lst.append(tag.string)


        for i in range(len(title_lst)):

            insert_info(title=title_lst[i],content=content_lst[i],time=date_lst[i],href=href_lst[i],source='eanquan')



    except Exception as a:
        pass
def anquanniu(flag=1):
    url='https://www.aqniu.com/'
    html = get_page(url, sflag=flag)
    try:
        mouthlist={"一月":'01',"二月":'02','三月':'03','四月':'04',"五月":'05','六月':'06','七月':'07','八月':'08','九月':'09','十月':'10','十一月':'11','十二月':'12'}
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('.post > div > div > h4 ')
        content = soup.select('.post > div > div > p ')
        date = soup.select('.post > div > div > div > span[class="date"]')
        href_lst = []
        content_lst = []
        title_lst = []
        date_lst = []
        if titles:
            for tag in titles:
                title_lst.append(tag.a.string)
                href_lst.append(tag.a['href'])
        if content:
            for tag in content:
                content_lst.append(tag.string)
        if date:
            for tag in date:
                s=tag.string.split(',')
                year=s[2][1:]
                mouth=mouthlist[s[1][1:3]]
                day=s[1][4:]
                time='-'.join([year,mouth,day])
                date_lst.append(time)
        for i in range(len(title_lst)):
            insert_info(title=title_lst[i], content=content_lst[i], time=date_lst[i], href=href_lst[i],
                        source='anquanniu')

    except Exception as a:
        pass


def cnvd(flag=1):
    url="http://www.cnvd.org.cn"
    html = get_page(url, sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('.t1_tab_b > ul > li > a')
        date=soup.find_all('span',class_='t1_sp_right')

        title_lst = []
        href_lst=[]
        date_lst=[]
        if titles:
            for tag in titles:
                title_lst.append(tag['title'])
                href_lst.append(url+tag['href'])

        if date:
            for tag in date:
                date_lst.append(tag.string.strip())
        # print(title_lst)
        # print(href_lst)
        # print(date_lst)

        for i in range(len(title_lst)):
            insert_info(title=title_lst[i], content='', time=date_lst[i], href=href_lst[i],
                        source='cnvd')

    except Exception as a:
        pass

def vdoo(flag=1):
    url='https://www.vdoo.com/blog/'
    html = get_page(url, sflag=flag)
    try:
        mouthlist={"January":'01',"February":'02','March':'03','April':'04',"May":'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}

        soup = BeautifulSoup(html, 'html.parser')
        titles=soup.find_all(class_='posts-group-item-title')
        content=soup.find_all(class_='posts-group-item-snippet')
        href=soup.select('a[style]')
        date=soup.find_all(class_='posts-group-item-date')
        title_lst = []
        content_lst=[]
        href_lst=[]
        date_lst=[]
        for tag in titles:
            title_lst.append(tag.string)
        for tag in content:
            content_lst.append(tag.string)
        for tag in href:
            href_lst.append('https://www.vdoo.com'+tag['href'])
        for tag in date:
            s = tag.string.split(',')
            year=s[1][1:]
            mouth=mouthlist[s[0].split(' ')[0]]
            day=s[0].split(' ')[1]
            time = '-'.join([year, mouth, day])
            date_lst.append(time)
        for i in range(len(title_lst)):
            insert_info(title=title_lst[i], content=content_lst[i], time=date_lst[i], href=href_lst[i],
                        source='vdoo')
    except Exception as a:
        pass

def mcw0(flag=1):
    url='https://github.com/mcw0/PoC'
    html = get_page(url, sflag=flag)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title=soup.find_all('h2')
        date_lst=[]
        for tag in title:
            date_lst.append(list(enumerate(tag.next_sibling.next_sibling))[0][1][:10])

        title_lst=[]
        href_lst=[]
        for tag in title:
            title_lst.append(tag.text)
            href_lst.append(url+tag.a['href'])
    #    print(href_lst)

        for i in range(len(title_lst)):
            insert_info(title=title_lst[i], content='', time=date_lst[i], href=href_lst[i],
                        source='bashis')
    except Exception as a:
        print(a)
        pass

def axis(flag=1):
    url='https://www.axis.com/en-hk/support/product-security'
    html=get_page(url, sflag=flag)

    try:
        soup = BeautifulSoup(html, 'html.parser')
        li= soup.find_all(class_='field-item')[3]
        li=li.select('li')

        title_lst = []
        href_lst = []
        date_lst = []
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for tag in li :
            href_lst.append(tag.a['href'])
            title_lst.append(tag.a.string)
        print(href_lst, title_lst)
        for i in range(len(title_lst)):
            insert_info(title=title_lst[i], content='', time=date, href=href_lst[i],
                        source='axis')
    except Exception as a:
        print(a)
        pass

if __name__ == '__main__':
    search_anquanke(0)
    search_ipvm(0)
    hik(0)
    yushi(0)
    cert(0)
    eanqun(0)
    anquanniu(0)
    cnvd(0)
    vdoo(0)
    mcw0(0)
    axis(0)
