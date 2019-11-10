from flask import Flask, render_template,session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))



CSRF_ENABLED = True
SECRET_KEY = 'adaeraserasdafds'


DEBUG = True
TESTING = True




app = Flask(__name__)
app.config['SECRET_KEY'] = 'Another_highly_secret_key' 
login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = "login"


bootstrap = Bootstrap(app)
app.config.from_object('config')

from app import views
