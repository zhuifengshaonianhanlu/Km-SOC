#coding:utf-8

from wtforms import Form,StringField,IntegerField,PasswordField
from wtforms.validators import EqualTo, Length, NumberRange, DataRequired, Email,ValidationError

from app.models.user import User

class AddUserForm(Form):
    '''
    check useradd
    '''
    username = StringField(validators=[DataRequired(message='username不能为空'),Length(2,10,message='用户名至少需要输入2~10个字符')])
    password = PasswordField(validators=[DataRequired(message='password不能为空'),Length(8,20,message='密码至少需要输入8~20个字符')])
    email = StringField(validators=[DataRequired(message='email不能为空'),Length(8,64),Email(message='邮件格式不对')])
    usertype = StringField(validators=[DataRequired(message='角色不能为空'),Length(1,message='用户类型为一位数字')])

    #验证唯一性,调用form.validate()时会自动进行验证
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已注册')


class LoginForm(Form):
    username = StringField(validators=[DataRequired(message='用户名不能为空'), Length(2, 10)])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(8, 20)])

