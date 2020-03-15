#!/usr/bin/python
# -*- coding: UTF-8 -*-


from flask import  render_template,redirect,request,url_for,flash,send_from_directory
from .form import LoginForm,SendEmailSet,AgentSet,SaveInfo
from . import auth
from .. import db
from flask_login import login_user,logout_user,login_required
from ..models import User,Info,Importinfo
import time
from sqlalchemy import or_,and_,extract
import json
import pickle

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next=request.args.get('next')
            if next is None or not next.startswith('/'):
                next=url_for('auth.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))

@auth.route('/index')
@login_required
def index():
    keyword = request.args.get('keyword')

    if keyword:
        data = []
        keywords = keyword.split(' ')
        for k in keywords:
            page = request.args.get('page', 1, type=int)
            pagination = Info.query.filter(Info.title.contains(k)).order_by(
                Info.time.desc()).paginate(page, max_per_page=15)
            data = data + pagination.items
        return render_template('auth/search.html', pagination=pagination, data=data, keyword=keyword)

    else:
        return render_template('auth/base_site.html')


@auth.route('/anquanke')
@login_required
def anquanke():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='anquanke').order_by(Info.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template("auth/anquanke.html", pagination=pagination, data=data)

@auth.route('/ipvm')
@login_required
def ipvm():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='ipvm').order_by(Info.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template('auth/ipvm.html', pagination=pagination, data=data)

@auth.route('/360cert')
@login_required
def cert():
    page=request.args.get('page',1,type=int)
    pagination=Info.query.filter(Info.source=="360cert").order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data=pagination.items
    return render_template("auth/360cert.html",pagination=pagination,data=data)

@auth.route('/youshang')
@login_required
def youshang():
    hik=Info.query.filter_by(source='hik')
    yushi=Info.query.filter_by(source='uniview')
    return render_template('auth/youshang.html',hik=hik,yushi=yushi)


@auth.route('/eanquan')
@login_required
def eanquan():
    page = request.args.get('page', 1, type=int)
    pagination=Info.query.filter(Info.source=="eanquan").order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data = pagination.items
    return render_template('auth/eanquan.html',pagination=pagination,data=data)

@auth.route('/cnvd')
@login_required
def cnvd():
    page = request.args.get('page', 1, type=int)
    pagination=Info.query.filter(Info.source=="cnvd").order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data = pagination.items
    return render_template('auth/cnvd.html',pagination=pagination,data=data)

@auth.route('/anquanniu')
@login_required
def anquanniu():
    page = request.args.get('page', 1, type=int)
    pagination=Info.query.filter(Info.source=="anquanniu").order_by(Info.time.desc()).paginate(page,max_per_page=15)
    data = pagination.items
    return render_template('auth/anquanniu.html',pagination=pagination,data=data)

@auth.route('/vdoo')
@login_required
def vdoo():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='vdoo').order_by(Info.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template("auth/vdoo.html", pagination=pagination, data=data)


@auth.route('/mcw0')
@login_required
def mcw0():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='bashis').order_by(Info.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template("auth/bashis.html", pagination=pagination, data=data)

@auth.route('/axis')
@login_required
def axis():
    page = request.args.get('page', 1, type=int)
    pagination = Info.query.filter_by(source='axis').order_by(Info.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template("auth/axis.html", pagination=pagination, data=data)


@auth.route('/report/<action>')
@login_required
def report(action):
    now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    weekId = time.strftime("%W")
    yearId = time.strftime("%Y")
    total = Info.query.filter(and_(extract('week', Info.time) == weekId),
                                   extract('year', Info.time) == yearId).all()
    week_count = Info.query.filter(and_(extract('week', Info.time) == weekId),
                                   extract('year', Info.time) == yearId).count()



    dahua = Info.query.filter(and_(extract('week',Info.time)== weekId,extract('year',Info.time)== yearId,or_(Info.title.contains('dahua'),Info.title.contains('大华'))))
    dahua_count=dahua.count()
    dahua_content=dahua.all()
    keyword=['hikvision','uniview','anxis','camera','海康','宇视','安迅士']
    youshang=[]
    youshang_count=0
    for key in keyword:
        info = Info.query.filter(and_(extract('week',Info.time)== weekId,extract('year',Info.time)== yearId,Info.title.contains(key)))
        youshang.extend(info.all())
        youshang_count=youshang_count+info.count()
    cert_count = Info.query.filter(and_(Info.source == '360cert', extract('week', Info.time) == weekId),
                                   extract('year', Info.time) == yearId).count()
    data={
        'time': now,
        'total': total,
        'week_count':week_count,
        'dahua_count':dahua_count,
        'dahua_content':dahua_content,
        'youshang_count':youshang_count,
        'youshang_content':youshang,
        'other_count': week_count-dahua_count-youshang_count,
        'total_content': total

    }
    if action == "export":
        import os
        import sys
        print(os.getcwd())
        try:
            with open('./app/templates/reportfile/html/out.html', 'w',encoding='utf-8') as fp:
                fp.write(render_template("auth/report/preview.html",data=data))
            os.system("wkhtmltopdf ./app/templates/reportfile/html/out.html ./app/templates/reportfile/pdf/out.pdf")
            return send_from_directory(os.getcwd()+'/app/templates/reportfile/pdf','out.pdf',as_attachment=True)
        except Exception as e:
            print(e)
            return "export falied"
    else:
        return render_template('auth/report/preview.html',data=data)


@auth.route('/config/')
@login_required
def config():

    with open('./config.ini', 'r') as fp:
        data = json.load(fp)
    form_SendEmail = SendEmailSet()
    form_agent = AgentSet()

    recvemail_list=data['recv_email']

    form_SendEmail.send_email.data=data['send_email_config']['send_email']
    form_SendEmail.smtp_server.data=data['send_email_config']['smtp_server']
    form_SendEmail.smtp_password.data=data['send_email_config']['smtp_password']

    form_agent.protocol.data=data['agent_set']['protocol']
    form_agent.addr.data=data['agent_set']['addr']
    form_agent.use.data=data['agent_set']['use']

    return render_template('auth/config/form.html',form_SendEmail=form_SendEmail,form_agent=form_agent,recvemail_list=recvemail_list)


@auth.route('/config/send_email',methods=['GET','POST'])
@login_required
def config_send_email():

    form_SendEmail=SendEmailSet()
    if form_SendEmail.validate_on_submit():
        send_email=form_SendEmail.send_email.data
        smtp_server=form_SendEmail.smtp_server.data
        smtp_password=form_SendEmail.smtp_password.data

        send_email_config={
            'send_email':send_email,
            'smtp_server':smtp_server,
            'smtp_password':smtp_password
        }
        with open('config.ini','r') as fp:
             data=json.load(fp)

        data['send_email_config']=send_email_config

        with open('config.ini','w') as fp:
            json.dump(data,fp)

    return redirect(url_for('auth.config'))


@auth.route('/config/agent_set',methods=['GET','POST'])
@login_required
def config_agent_set():

    form_agent = AgentSet()

    if form_agent.validate_on_submit():
        protocol=form_agent.protocol.data
        addr=form_agent.addr.data
        use=form_agent.use.data
        agent_set={
            'protocol':protocol,
            'addr':addr,
            'use' :use
        }
        with open('config.ini','r') as fp:
             data=json.load(fp)
        data['agent_set']=agent_set
        with open('config.ini','w') as fp:
            json.dump(data,fp)

    return redirect(url_for('auth.config'))

@auth.route('/config/email_set',methods=['GET','POST'])
@login_required
def config_email_set():
    if request.method == 'POST':
        data = json.loads((request.get_data()).decode('utf-8'))

        with open('config.ini','r') as fp:
             config_data=json.load(fp)

        if data['action']=='add':
            if data['recvemail'] not in config_data['recv_email']:
                config_data['recv_email'].append(data['recvemail'])
                with open('config.ini', 'w') as fp:
                    json.dump(config_data, fp)

        elif data['action']=='delete':
            config_data['recv_email'].remove(data['recvemail'])
            with open('config.ini', 'w') as fp:
                json.dump(config_data, fp)

    return redirect(url_for('auth.config'))

@auth.route('/importinfo/')
@login_required
def importinfo():
    page = request.args.get('page', 1, type=int)
    pagination = Importinfo.query.order_by(Importinfo.time.desc()).paginate(page, max_per_page=15)
    data = pagination.items
    return render_template('auth/saveinfo/importinfo.html',pagination=pagination, data=data)


@auth.route('/saveinfo/')
@login_required
def saveinfo():
    form_save=SaveInfo()
    return render_template('auth/saveinfo/saveinfo.html',form_save=form_save)



@auth.route('/save/',methods=['GET','POST'])
@login_required
def save():
    import os
    stauts={"code":0,'message':'falsed'}
    if request.method == 'POST':
        data = json.loads((request.get_data()).decode('utf-8'))
        title=data['title']
        href=data['href']
        time=data['time']
        info=Importinfo.query.filter_by(title=title).first()
        stauts = {"code": 0, 'message': 'already exist'}
        if info is None:
            info=Importinfo(title=title,href=href,time=time)
            
            try:
                db.session.add(info)
                db.session.commit()
                stauts['code'] = '1'
                stauts['message']='secuess'
                stauts = json.dumps(stauts)
                cmd ="wkhtmltopdf "+ href +" ./app/templates/reportfile/pdf/"+title+".pdf"
                os.system(cmd)
                return stauts
            except Exception as e:
                stauts['code']=0
                stauts['message']=str(e)

    stauts=json.dumps(stauts)
    return stauts

@auth.route('/delete/',methods=['GET','POST'])
@login_required
def delete():
    import os
    if request.method == 'POST':
        data = json.loads((request.get_data()).decode('utf-8'))
        print(data)
        title=data['title']
        print(title)
        try:
            Importinfo.query.filter_by(title=title).delete()
            path = "./app/templates/reportfile/pdf/"+title+".pdf"
            os.remove(path)
            return "success"
        except Exception as a:
            return str(a)

    return "falsed"


