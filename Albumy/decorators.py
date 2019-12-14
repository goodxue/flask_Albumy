'''
@Time    :   2019/12/14 21:49:54
'''
__AUTHOR__ = 'xwp' 

from flask import Markup, flash, url_for, redirect
from functools import wraps
from flask_login import current_user

def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            messaage = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email')
            )
            flash(message,'warning')
            return redirect(url_for('main.index'))
        return func(*args,**kwargs)
    return decorated_function
