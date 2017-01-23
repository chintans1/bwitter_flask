from flask_login import LoginManager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
app.jinja_env.globals['momentjs'] = momentjs
