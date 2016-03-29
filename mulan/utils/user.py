#-*- coding: utf-8 -*-
import time
import base64
import hashlib
import functools
from flask import g, request, session, current_app
from flask import flash, url_for, redirect, abort
from ..models import Account
__author__ = 'Simi'


class require_role(object):
    roles = {
        'spam': 0,
        'new': 1,
        'user': 10,
        'staff': 80,
        'admin': 100,
    }

    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                url = url_for('account.signin')
                if '?' not in url:
                    url += '?next=' + request.url
                return redirect(url)
            if g.user.get('state') == 2:
                flash('您的账户已经被管理员禁止使用了', 'danger')
                return redirect(url_for('account.signout',next=url_for('front.index')))
            if self.role is None:
                return method(*args, **kwargs)
            # if g.user.id == 1:
            #     # this is superuser, have no limitation
            #     return method(*args, **kwargs)
            # if g.user.role == 'new':
            #     flash('Please verify your email', 'warn')
            #     return redirect('/account/settings')
            # if g.user.role == 'spam':
            #     flash('You are a spammer', 'error')
            #     return redirect('/')
            # if self.roles[g.user.role] < self.roles[self.role]:
            #     return abort(403)
            roles = g.user.get('roles')
            if self.role not in roles:
                abort(403)
            return method(*args, **kwargs)
        return wrapper


require_login = require_role(None)
require_user = require_role('user')
require_staff = require_role('staff')
require_admin = require_role('admin')


def get_current_user():
    if 'id' in session and 'token' in session:
        # current = User().get_current()
        # if not current:
        #     return None
        # if current._session_token != session['token']:
        #     return None
        # return current

        user = Account.get(session['id'])
        if not user:
            return None
        # TODO: 验证token
        # if user._session_token != session['token']:
        #     return None
        return user
    return None


def login_user(user, permanent=False):
    if not user:
        return None
    session['id'] = user.id
    session['token'] = user._session_token
    if permanent:
        session.permanent = True
    return user


def logout_user():
    if 'id' not in session:
        return
    session.pop('id')
    session.pop('token')


def create_auth_token(user):
    timestamp = int(time.time())
    secret = current_app.secret_key
    token = '%s%s%s%s' % (secret, timestamp, user.id, user.token)
    hsh = hashlib.sha1(token).hexdigest()
    return base64.b32encode('%s|%s|%s' % (timestamp, user.id, hsh))


def verify_auth_token(token, expires=30):
    try:
        token = base64.b32decode(token)
    except:
        return None
    bits = token.split('|')
    if len(bits) != 3:
        return None
    timestamp, user_id, hsh = bits
    try:
        timestamp = int(timestamp)
        user_id = int(user_id)
    except:
        return None
    delta = time.time() - timestamp
    if delta < 0:
        return None
    if delta > expires * 60 * 60 * 24:
        return None

    user = Account.query.get(user_id)
    if not user:
        return None
    secret = current_app.secret_key
    _hsh = hashlib.sha1('%s%s%s%s' % (secret, timestamp, user_id, user.token))
    if hsh == _hsh.hexdigest():
        return user
    return None
