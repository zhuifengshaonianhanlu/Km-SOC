#coding:utf-8

import datetime
from flask import Blueprint,render_template,request,redirect,url_for,flash,jsonify,session
from flask_login import login_user, logout_user, current_user, login_required,UserMixin,login_manager
from werkzeug.security import generate_password_hash,check_password_hash

from app.forms.formcheck import AddUserForm,LoginForm
from app.models.user import User,get_uid,validateEmail
from app.models.base import db



'''
user manager:useradd,login,logout
'''

user = Blueprint('user',__name__)


@user.route('/usermg',methods=['GET','POST'])
@login_required
def usermg():
    rs = User.query.all()
    userlist = []
    for user in rs:
        ctime = user.ctime
        username = user.username
        email = user.email
        usertype = user.usertype
        if usertype == 1:
            usertype = '管理员'
        if usertype == 2:
            usertype = '普通用户'
        uid = user.uid
        userlist.append({'ctime':ctime,'username':username,'email':email,'usertype':usertype,'uid':uid})

    return render_template('user/user.html',userlist=userlist)


@user.route('/deluser',methods=['POST'])
@login_required
def deluser():
    try:
        postdata = request.get_json()
        uid = postdata['uid']
        User.query.filter_by(uid=uid).delete()
        db.session.commit()
    except BaseException as e:
        return jsonify({'result':'请求错误'})
    else:return jsonify({'result':'删除成功'})


@user.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    if request.method == 'POST':
        try:
            userdata = request.get_json()
            username = userdata['username']
            password = userdata['password']
            email = userdata['email']
            usertype = userdata['usertype']

            if usertype not in ['1','2']:
                return jsonify({'result':'usertype error!'})
            if len(password) < 8:
                return jsonify({'result':'密码请搞到8位以上'})
            if not validateEmail(email):
                return jsonify({'result':"email格式错误"})

            Ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            uid = get_uid(username)

            userinfo = User(ctime=Ctime,username=username,
                            password=generate_password_hash(password),email=email,usertype=usertype,uid=uid)

            db.session.add(userinfo)
            db.session.commit()
        except BaseException as e:
            return jsonify({'reuslt':'请求错误'})
        return jsonify({'result':'添加成功'})


@user.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        userinfo = User.query.filter_by(username=username).first()

        if userinfo and check_password_hash(generate_password_hash(password),password):

            # 把用户的id号写入到cookie中，通过get_id获取用户的id，用户模型中需要有这个函数
            # remember=true，cookie会持续性的生效，默认是365天
            # duration会生成一个remember的cookie
            # session.permanent = True
            # user.permanent_session_lifetime = datetime.timedelta(minutes=1)

            login_user(userinfo,remember=True,duration=datetime.timedelta(hours=48))

            # 全局把用户名写入到session，供统一通过session调用
            session['username'] = username

            #next会在登录成功后自动在url中以参数形式回调,next是访问的需要授权的页面，登录完成后，会自动跳转回去
            next = request.args.get('next')
            if not next or not next.startwith('/'):
                next = url_for('index.indexpage')
            return redirect(next)
        else:
            flash('账号或者密码错误')
    return render_template('login.html')


@user.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('user.login'))