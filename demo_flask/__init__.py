from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from demo_flask.database import db_session
from demo_flask.models import User, Role
from flask_security import Security, SQLAlchemySessionUserDatastore, login_required
from flask_security.decorators import roles_required
from flask_security.core import current_user
from datetime import timedelta


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'jini-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'jini-salt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'disabled'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

CSRFProtect(app)

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


@app.route('/login', methods=['GET'])
def login():
    return render_template('security/login_user.html')


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('views/main.html', title='home')


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
    return redirect(url_for('login'))
