from flask_login import LoginManager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .momentjs import momentjs
import sys
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from app import views, models
app.jinja_env.globals['momentjs'] = momentjs
