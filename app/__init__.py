from flask import Flask
from core import *
from github import Github
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

Tools = Tools()
Git = Git(Github)
Content = Content()
Section = Section()

from app import views, models