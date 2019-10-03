'''
@Time    :   2019/10/03 20:39:58
'''
__AUTHOR__ = 'xwp' 

import os
import click

from flask import Flask, render_template, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from Albumy.settings import config
from Albumy.extensions import db
from Albumy.models import User

#创建app,并且和一系列扩展绑定
def create_app(config_name=None):
    if config_name is None:
        comfig_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('albumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_commands(app)  #注册命令行工具

    return app

def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def init():
        """Initialize Albumy."""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')
    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    def forge(user):
        """Generate fake data."""

        from Albumy.fake import fake_user

        db.drop_all()
        db.create_all()

        click.echo('Generating %d users...' % user)
        fake_admin()
        click.echo('Done.')