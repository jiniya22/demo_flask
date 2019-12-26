from flask import Flask, render_template, redirect, url_for
from flask_security import RoleMixin, UserMixin, Security, SQLAlchemySessionUserDatastore, login_required
from flask_wtf.csrf import CSRFProtect
from flask_security.decorators import roles_required
from flask_security.core import current_user

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine('mysql+mysqldb://test:test@localhost:3306/jiniworld_flask?charset=utf8', echo=False, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'jini-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'jini-salt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'disabled'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'


CSRFProtect(app)

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    description = Column(String(50))

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

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# @app.before_first_request
# def create_user():
#     from flask_security.utils import hash_password
#
#     db.create_all()
#     user_datastore.create_user(email='yeonjini2222@gmail.com', password=hash_password('1'), name='jini')
#     user_datastore.create_role(name='ROLE_VIEW', description='demo 페이지 보기 권한')
#     db.session.commit()

# Views
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('views/main.html', title='view main')


@app.route('/login')
def login():
    return render_template('security/login_user.html')


@app.route('/users')
@login_required
@roles_required('ROLE_ADMIN')
def users():
    args = {'title': 'users', 'msg': '사용자 정보는 ROLE_ADMIN 권한을 보유한 사용자만 조회할 수 있다.'}
    return render_template('views/main.html', **args)


@app.route('/stores')
@login_required
@roles_required('ROLE_VIEW')
def stores():
    return render_template('views/main.html', title='stores')


@app.route('/logout', methods=['POST'])
def logout():
    from flask_security.utils import logout_user
    logout_user()
    return redirect(url_for('home'))    # FIXME

# @app.route("/")
# def index():
#     return redirect(url_for('login'))
#
#
# @app.route("/login")
# def loginPage():
#     return render_template('index.html')
#
#
# @app.route("/login", methods=['POST'])
# def login():
#     from flask import request
#     from dotmap import DotMap
#     value = DotMap(request.form)
#     return render_template('views/main.html', email=value.email)

