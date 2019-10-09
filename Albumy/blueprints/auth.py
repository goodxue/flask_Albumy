from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from albumy.extensions import db
from albumy.forms.auth import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from albumy.models import User
from albumy.settings import Operations

from Albumy.settings import Operations
from Albumy.utils import generate_token, validate_token
#from Albumy.email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name,email=email,username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        # token = generate_token(user=user,operation=Operations.CONFIRM)
        # send_confirm_account_email(user=user,token=token)
        # flash('Confirm email sent, check your inbox','info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('Account confirmed.','success')
        return rediredct(url_for('main.index'))
    else:
        flash('Invalid or expired token.','danger')
        return redirect(url_for('.resend_confirm'))