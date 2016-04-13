# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, jsonify, request, redirect, url_for, g, \
    flash, current_app

from leancloud import Query

from ..utils.user import require_login, require_admin
from ..models import Account
from ..forms import SearchAccountForm, EditAccountForm
from ..utils.helpers import force_int

__author__ = 'Simi'
__all__ = ['bp']
bp = Blueprint('admin', __name__)


@bp.route('/')
@require_login
def index():
    return render_template('admin/index_type.html')


@bp.route('/user')
@require_login
@require_admin
def user():
    page = force_int(request.args.get('page', 1), 1)
    page_size = 10

    q = Query("_User")

    search_form = SearchAccountForm()

    keyword = None
    if request.method == 'GET':
        search_form.keyword.data = keyword = request.args.get('keyword', '')

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data.strip()

    if keyword:
        if "@" in keyword:
            q = q.startswith("email", keyword)
        else:
            q = q.startswith("username", keyword)

    users = q.skip((page - 1) * page_size).limit(page_size).find()
    count = q.count()
    pages = count / page_size + 1

    return render_template('admin/user.html', users=users, form=search_form, count=count, pages=pages, page=page)


@bp.route('/user/edit/<string:id>', methods=['GET', 'POST'])
@require_login
@require_admin
def edit_user(id):
    user = Account.get(id)
    if not user:
        abort(404)
    form = EditAccountForm(obj=user)

    if form.validate_on_submit():
        user.set('state', form.state.data)
        user.set('roles', [form.role.data])
        user.save()
        flash('用户 %s 的信息已成功保存' % user.get('username'), 'success')
        return redirect(url_for('.user'))
    else:
        roles = user.get('roles')
        if roles:
            # 当前仅支持一个用户拥有一种角色
            form.role.data = roles[0]
        state = user.get('state')
        if state:
            form.state.data = state
    return render_template('admin/edit_user.html', form=form, user=user)
