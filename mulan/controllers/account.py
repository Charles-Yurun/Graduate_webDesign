# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, abort, jsonify, redirect, \
    url_for, g, flash, current_app
from ..utils.user import login_user, logout_user, verify_auth_token, require_login
from ..forms import SigninForm, SignupForm, ChangePasswordForm, FindForm
from ..utils.mail import signup_mail, find_mail

__author__ = 'Simi'
__all__ = ['bp']

bp = Blueprint('account', __name__)


# @bp.errorhandler(Exception)
# def handle_exception(e):
#     # TODO: LOG
#     traceback.print_exc()
#     # flash('You give us a problem, we will solve as soon as possible.', 'error')
#     abort(501)

@bp.route('/')
@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page."""
    # next_url = request.args.get('next', url_for('front.index'))
    next_url = request.args.get('next', url_for('admin.index'))
    if g.user:
        return redirect(next_url)
    form = SigninForm()
    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return redirect(next_url)
    return render_template('account/signin.html', form=form, next_url=next_url)


@bp.route('/signout')
def signout():
    """Sign out, and redirect."""
    next_url = request.args.get('next', url_for('account.signin'))
    logout_user()
    return redirect(next_url)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page. If the request has an token arguments, it is not
    for registeration, it is for verifying the token.
    """
    next_url = request.args.get('next', url_for('front.index'))
    token = request.args.get('token')
    if token:
        user = verify_auth_token(token, 1)
        if not user:
            flash('Invalid or expired token.', 'error')
            return redirect(next_url)
        user.role = 'user'
        user.save()
        login_user(user)
        flash('This account is verified.', 'success')
        return redirect(next_url)

    form = SignupForm()
    if form.validate_on_submit():
        verify_email = current_app.config.get('VERIFY_EMAIL', True)
        if not verify_email:
            # if no need for verify email
            # we should save the role as new
            user = form.save('new')
            login_user(user)
            return redirect(next_url)
        user = form.save('new')
        login_user(user)
        # msg = signup_mail(user)
        # if current_app.debug:
        #     return msg.html
        # flash('We have sent you an activate email, check your inbox.','info')
        return redirect(next_url)
    return render_template('account/signup.html', form=form)


@bp.route('/setting', methods=['GET', 'POST'])
@require_login
def setting():
    """Settings page of current user."""
    form = ChangePasswordForm()
    return render_template('account/setting.html', password_form=form)


@bp.route('/password', methods=['GET', 'POST'])
@require_login
def change_password():
    """Change password page."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        flag = g.user.check_password(form.old_password.data)
        if flag:
            g.user.change_password(form.new_password.data).save()
            login_user(g.user)
            flash('密码已修改，请牢记修改后的新密码。', 'success')
            return redirect(url_for('.setting'))
        else:
            flash('密码修改失败，请稍后重试。', 'error')
    return render_template('account/setting.html', password_form=form)


@bp.route('/find', methods=['GET', 'POST'])
def find():
    """重置密码"""
    if g.user:
        return redirect('/')
    form = FindForm()
    if form.validate_on_submit():
        msg = find_mail(form.user)
        if current_app.debug or current_app.testing:
            return msg.html
        flash('邮件发送成功', 'info')
        return redirect(url_for('.signin'))
    return render_template('account/find.html', form=form)
