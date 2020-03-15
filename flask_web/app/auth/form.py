#!/usr/bin/python
# -*- coding: UTF-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired,Email,URL

class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Log In')

class SendEmailSet(FlaskForm):
    send_email=StringField('Send_Email',validators=[DataRequired(),Email()])
    smtp_server=StringField('SMTP Server',validators=[DataRequired(),URL()])
    smtp_password=StringField('SMTP Server Code',validators=[DataRequired()])
    submit1=SubmitField('save')

class AgentSet(FlaskForm):
    protocol=SelectField(u'Protocol Select',validators=[DataRequired()],choices=[(1,'http'),(2,'https')],default=1,coerce=int)
    addr=StringField('Proxy Addr',validators=[DataRequired(),URL()])
    use=BooleanField('Start')
    submit2=SubmitField('save')

class SaveInfo(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    href=StringField('Href',validators=[DataRequired,URL()])
    time=StringField('Date',validators=[DataRequired()])
