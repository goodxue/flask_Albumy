from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from Albumy.models import User

#用户名作为个人主页的url，所以必须唯一，不能重名
class RegisterForm(FlaskForm): #想法：做成app的话表单也是可以使用的，将前端传来的json转成form自动验证
    name = StringField('Name', validators=[DataRequired(),Length(1,30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
        Regexp('^[a-zA-Z0-9]*$',message='The username should cotain only a-z,A-Z and 0-9')])
    password = PasswordField('Password',validators=[
        DataRequired(), Length(8,128),EqualTo('Password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already in use.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')
