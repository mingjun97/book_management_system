from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.debug = True
app.template_folder = 'templates'
app.static_folder = 'templates/static'
app.config['SECRET_KEY'] = 'L1bR4rY_M4N4g3m3nt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/library?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PER_PAGE'] = 10
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "app.view.login"

from .view import view as view_blueprint
app.register_blueprint(view_blueprint)

from app.models import Admin


@login_manager.user_loader
def load_user(userid):
    return Admin.get(userid)