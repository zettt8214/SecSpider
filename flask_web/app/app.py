# -*- coding: UTF-8 -*-

from flask import Flask,render_template
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('1.html')

@app.route('/data')
def data():
    data= {
        'code':'success',
        'items':[
            {
                'name':'直接访问',
                'value': 335
            },
            {
                'name': '邮件营销',
                'value': 310
            },
            {
                'name': '联盟广告',
                'value': 234
            },
            {
                'name': '视频广告',
                'value': 135
            },
            {
                'name': '搜索引擎',
                'value': 1548
            }
        ]
    }

    data=json.dumps(data)
    return data


if __name__ == '__main__':
    app.run()
