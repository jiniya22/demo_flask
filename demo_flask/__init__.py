from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin, Security, SQLAlchemyUserDatastore, login_required
from flask_wtf.csrf import CSRFProtect
from flask_security.decorators import roles_required
from flask_security.core import current_user


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'jini-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'jini-salt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqldb://test:test@localhost:3306/jiniworld_flask?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'disabled'

CSRFProtect(app)

db = SQLAlchemy(app)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(50))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(50))
    create_timestamp = db.Column(db.DateTime())
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
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

