#coding:utf-8

import datetime
from flask import Blueprint,render_template,request,redirect,url_for,flash,jsonify
from flask_login import login_user, logout_user, current_user, login_required,UserMixin,login_manager
from app.forms.formcheck import AddUserForm,LoginForm

from app.models.user import User
from app.models.user import db
from werkzeug.security import generate_password_hash,check_password_hash


'''
user manager:useradd,login,logout
'''

auth = Blueprint('auth',__name__)


@auth.route('/adduser',methods=['GET','POST'])
def adduser():
    #实例化AddUserForm这个类
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate():
        postdata = form.data
        Ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #check:result = check_password_hash(password, raw_password)
        userinfo = User(ctime=Ctime,username=postdata.get('username'),password=generate_password_hash(postdata.get('password')))

        db.session.add(userinfo)
        db.session.commit()
        return jsonify({'msg':'add user success'})
    return render_template('adduser.html',form=form)


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(form.password.data):
            return jsonify({'msg':'login success'})
            login_user(user,remember=True)
            #next会在登录成功后自动在url中以参数形式回调
            next = request.args.get('next')
            if not next or not next.startwith('/'):
                next = url_for('login')
            return redirect(next)
        else:
            flash('账号或者密码错误')
    return render_template('login.html')

