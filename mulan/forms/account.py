# -*- coding: utf-8 -*-
import sys
from flask import current_app

from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField, \
    SelectField, HiddenField, validators
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional, URL
from ._base import BaseForm
from ..models import Account

from leancloud import User

__author__ = 'Simi'

reload(sys)
sys.setdefaultencoding('utf-8')

__all__ = [
    'SignupForm', 'SigninForm', 'ChangePasswordForm', 'SearchAccountForm', 'EditAccountForm', 'FindForm'
]

RESERVED_WORDS = [
    'root', 'bot', 'robot', 'master', 'webmaster',
    'account', 'people', 'user', 'users', 'project', 'projects',
    'search', 'action', 'favorite', 'like', 'love', 'none',
    'team', 'teams', 'group', 'groups', 'organization',
    'organizations', 'package', 'packages', 'org', 'com', 'net',
    'help', 'doc', 'docs', 'document', 'documentation', 'blog',
    'bbs', 'forum', 'forums', 'static', 'assets', 'repository',

    'public', 'private',
    'mac', 'windows', 'ios', 'lab',
]


class SignupForm(BaseForm):
    username = StringField(
            '用户名',
            validators=[
                DataRequired(message="请输入用户名"), Length(min=4, max=18, message="由4-18个字母、数字组成"),
                Regexp(r'^[a-z0-9A-Z]+$')
            ], description='用户名',
    )
    email = EmailField(
            '邮箱',
            validators=[DataRequired(message="请输入邮箱"), Email(message="请输入正确的邮箱")],
            description='邮箱'
    )
    password = PasswordField(
            '密码',
            validators=[DataRequired(message="请输入密码"), Length(min=6, max=16, message="长度为6-16个字符")],
            description='密码'
    )
    confirm_password = PasswordField(
            '确认密码',
            validators=[DataRequired(message="请输入确认密码"), Length(min=6, max=16, message="长度为6-16个字符")],
            description='确认密码'
    )
    agree = BooleanField('阅读并同意相关服务条款和隐私政策')

    def validate_username(self, field):
        data = field.data.lower()
        if '%' in data:
            raise ValueError("用户名不能包含字符 '%'")
        if data in RESERVED_WORDS:
            raise ValueError('不允许注册此用户名')
        if data in current_app.config.get('RESERVED_WORDS', []):
            raise ValueError('不允许注册此用户名')

        if Account.get_by_username(data):
            raise ValueError('用户名已经被注册')

    def validate_email(self, field):
        if Account.get_by_email(field.data):
            raise ValueError('这个邮箱已经注册过了')

    def validate_confirm_password(self, filed):
        if filed.data != self.password.data:
            raise ValueError('确认密码和密码不一致')

    def validate_agree(self, field):
        if not field.data:
            raise ValueError('请阅读并同意相关服务条款和隐私政策')

    def save(self, role=None):
        # user = Account(**self.data)
        # if role:
        #     user.role = role
        # user.nickname = user.username
        # user.save()
        # return user
        from leancloud import User
        user = User()
        user.set("username", self.username.data.lower().strip())
        user.set("password", self.password.data)
        user.set("email", self.email.data.strip())
        if role:
            user.set('roles', [role])

        # other fields can be set just like with leancloud.Object
        # user.set("phone", "415-392-0202")
        user.sign_up()

        return user


class SigninForm(BaseForm):
    account = StringField(
            '账号',
            validators=[DataRequired(), Length(min=4, max=200)],
            description='用户名或者邮箱'
    )
    password = PasswordField(
            'Password', validators=[DataRequired()],
            description='密码'
    )
    permanent = BooleanField('记住我')

    def validate_account(self, field):
        if not Account.get_by_username(field.data) and not Account.get_by_email(field.data):
            raise ValueError("账号不存在")

    def validate_password(self, field):
        user = User()
        try:
            user.login(self.account.data.strip(), self.password.data)
            self.user = user
        except Exception, e:
            if e.code:
                if e.code == 210:
                    raise ValueError('用户名/密码不正确')
                if e.code == 211:
                    raise ValueError('账号不存在')
            raise ValueError('用户名/密码不正确')

            # def validate_password(self, field):
            #     account = self.account.data
            #     if '@' in account:
            #         user = Account.query.filter_by(email=account).first()
            #     else:
            #         user = Account.query.filter_by(username=account).first()
            #
            #     if not user:
            #         raise ValueError('用户名/密码不正确')
            #     if user.check_password(field.data):
            #         self.user = user
            #         user.active = datetime.utcnow()
            #         user.save()
            #         return user
            #     raise ValueError('用户名/密码不正确')


class ChangePasswordForm(BaseForm):
    old_password = PasswordField(
            '当前密码', validators=[DataRequired(message="请输入当前密码")],
            description='请输入当前密码'
    )
    new_password = PasswordField(
            '新的密码',
            validators=[DataRequired(message="请输入新的密码"), Length(min=6, max=16, message="长度为6-16个字符")],
            description='请输入新的密码'
    )
    confirm_password = PasswordField(
            '确认密码',
            validators=[DataRequired(message="请输入确认密码"), Length(min=6, max=16, message="长度为6-16个字符")],
            description='请输入确认密码'
    )

    def validate_old_password(self, filed):
        from flask import g
        if not g.user.check_password(filed.data):
            raise ValueError("密码错误")

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValueError("新的密码和确认密码不一致")


class SearchAccountForm(BaseForm):
    keyword = StringField("keyword", description="用户名 或者 邮箱")


class EditAccountForm(BaseForm):
    state = SelectField(
            '状态',
            coerce=int,
            choices=[(1, '正常'), (2, '禁用')],
            default=0,
            validators=[DataRequired()]
    )
    role = SelectField(
            '角色',
            choices=[('user', '用户'), ('new', '新用户'), ('admin', '管理员')],
            validators=[DataRequired()]
    )


class FindForm(BaseForm):
    account = StringField(
            '账号', validators=[DataRequired()],
            description='用户名 或者 注册邮箱'
    )

    def validate_account(self, field):
        account = field.data
        if '@' in account:
            user = Account.query.filter_by(email=account).first()
        else:
            user = Account.query.filter_by(username=account).first()
        if not user:
            raise ValueError('账号不存在')
        self.user = user
