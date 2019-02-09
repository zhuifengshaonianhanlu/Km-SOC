#coding:utf-8


from flask import jsonify,Blueprint,request,render_template
from flask_login import current_user,login_required

spider = Blueprint('spider',__name__)


@spider.route('/spider')
# @login_required
def spider_data():
    return 'logged in as: %s' % current_user.get_id()