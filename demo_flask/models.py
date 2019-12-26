from demo_flask.database import Base
from flask_security import RoleMixin, UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    description = Column(String(50))

    def __repr__(self):
        return '<Role %r> %r %r' % (self.id, self.name, self.description)


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(150))
    name = Column(String(50))
    create_timestamp = Column(DateTime())
    active = Column(Boolean())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r> %r %r' % (self.id, self.name, self.email)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

    def __repr__(self):
        return '<RolesUsers %r> %r %r' % (self.id, self.user_id, self.role_id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id
        }
