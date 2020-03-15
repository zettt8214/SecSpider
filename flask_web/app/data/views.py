#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import  render_template
from . import data
from flask_login import login_required
from app.models import Info
from sqlalchemy import or_,and_,extract
import json
import time

@data.route('/echarts')
@login_required
def echarts():
    return render_template("data/echarts.html")

@data.route('/count')
def count():
    weekId = time.strftime("%W")
    yearId = time.strftime("%Y")
    total=Info.query.count()
    week_count=Info.query.filter(and_(extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()

    ipvm_count = Info.query.filter(and_(Info.source =='ipvm',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()
    anquanke_count = Info.query.filter(and_(Info.source =='anquanke',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()
    youshang_count = Info.query.filter(or_(and_(Info.source =='hik',extract('week',Info.time)==weekId,extract('year',Info.time)==yearId), and_(Info.source =='uniview',extract('week',Info.time)==weekId,extract('year',Info.time)==yearId))).count()
    cert_count = Info.query.filter(and_(Info.source =='360cert',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()
    eanquan_count= Info.query.filter(and_(Info.source =='eanquan',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()
    anquanniu_count= Info.query.filter(and_(Info.source =='anquanniu',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()
    cnvd_count= Info.query.filter(and_(Info.source =='cnvd',extract('week',Info.time)==weekId),extract('year',Info.time)==yearId).count()

    data= {
        'code':'success',
        'total':total,
        'weekcount':week_count,
        'items':[
            {
                'name':'IPVM',
                'value': ipvm_count
            },
            {
                'name': '安全客',
                'value': anquanke_count
            },
            {
                'name': 'IoT厂商安全公告',
                'value': youshang_count
            },
            {
                'name': '360cert',
                'value': cert_count
            },
            {
                'name':'e安全',
                'value':eanquan_count
            },
            {
                'name':'安全牛',
                'value':anquanke_count
            },
            {
                'name':'cnvd',
                'value':cnvd_count
            }
        ]
    }

    data=json.dumps(data)
    return data


