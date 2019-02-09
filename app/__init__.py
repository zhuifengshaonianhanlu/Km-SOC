#coding:utf-8

"""
Author:hanlu
"""

from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from datetime import timedelta

#初始化flask核心对象，把一些全局的需要初始化的操作放在这里进行

login_manager = LoginManager()


def create_app():
    app = Flask(__name__,template_folder= 'templates',static_folder='templates/assets')
    app.config.from_object('app.setting')

    register_blueprint(app)  #所有的api都在这里进行blueprint注册

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = '请先登录或注册'


    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web.user import user
    from app.web.kmeye import kmeye
    from app.web.nav import nav
    from app.web.download import download
    from app.web.index import index

    app.register_blueprint(user)
    app.register_blueprint(kmeye)
    app.register_blueprint(nav)
    app.register_blueprint(download)
    app.register_blueprint(index)

