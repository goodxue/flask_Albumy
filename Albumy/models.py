'''
@Time    :   2019/10/03 20:52:55
'''
__AUTHOR__ = 'xwp' 

from datetime import datetime
from flask_login import UserMixin  #该类提供几个存储用户资料的字段，和存储用户账户的确认字段
from werkzeug.security import generate_password_hash, check_password_hash

from Albumy.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        self.set_role()

    def set_role():


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Colum(db.String(30),unique=True)
    users = db.relationship('User',back_populates='role')
    permissions = db.relationship('Permission',secondary=roles_permissions,back_populates='roles')
    @staticmethod
    def init_role():
        roles_permission_map={
            'Locked';['FLOOLW','COLLECT'],
            'User':['FOLLOW','COLLECT','COMMENT','UPLOAD'],
            'Moderator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE'],
            'Administrator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE','ADMINISTER']
        }

        for role_name in roles_permission_map:
            role = Role.query.filter_by(name=role_name).first()
            if role = Role(name=role_name)
            db.session.add(role)
        role.permissions = []
        for permission_name in roles_permission_map[role_name]:
            permission = Permission.query.filter_by(name=permission_name).first()
            if permission is None:
                permission = Permission(name=permission_name)
                db.session.add(permission)
            role.permissions.append(permission)
        db.session.commit()

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(30),unique=True)
    roles = db.relationship('Role',secondary=roles_permission, back_populations='permissions')

