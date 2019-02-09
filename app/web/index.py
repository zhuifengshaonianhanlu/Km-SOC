#coding:utf-8

"""
Author:hanlu

"""

from flask import jsonify,Blueprint,request,render_template,flash,make_response
from flask_login import login_required,current_user
from app.models.user import User

index = Blueprint('index',__name__)


@index.route('/index',methods=['GET'])
@login_required
def indexpage():
    # username = User.query.filter_by(id=current_user.get_id()).first().username
    return render_template('index.html')