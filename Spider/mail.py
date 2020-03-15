#!/usr/bin/python 
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import re
import json

with open('config.ini', 'r') as fp:
    config_data = json.load(fp)
send_mail_config=config_data['send_email_config']
recv_email=config_data['recv_email']


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail(title,href,source,time,content=''):


    form_addr=send_mail_config['send_email']
    # 不是邮箱密码,而是开启SMTP服务时的授权码


    password=send_mail_config['smtp_password']

    # 收件人的邮箱

    to_addr=recv_email
    print(to_addr)
    # qq邮箱的服务器地址

    #smpt_server = 'smtp.163.com'
    smpt_server=send_mail_config['smtp_server']
    #print(form_addr,password,to_addr)
    messag='<html><head></head><body><h1><a href=%s>%s</a></h1><p>%s</p></br>time:%s 来源：%s</body></html>'%(href,title,content,time,source)
    # 设置邮件信息
    msg = MIMEText(messag, 'html', 'utf-8')
    msg['From'] = _format_addr(u'安全监控 <%s>' %form_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' %to_addr)

    msg['Subject'] = Header(u'安全预警', charset='utf-8').encode()

    # 发送邮件
    server = smtplib.SMTP_SSL(smpt_server, port=994)
    server.set_debuglevel(1)
    server.login(form_addr, password)
    server.sendmail(form_addr, to_addr, msg.as_string())
    server.quit()

if __name__ == '__main__':

    title='Dahua Dual '
    a = re.search(r'windows|hik|hikvision|uniview|vuln|axis', title, re.IGNORECASE)
    if a.group():
        send_mail('dahua','http://www.ipvm.com','ipvm','2018-10-31','test')
