from flask import Flask
from core import *
from github import Github
from flask.ext.sqlalchemy import SQLAlchemy
import sys
import logging

app = Flask(__name__)
app.config.from_object('config')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
db = SQLAlchemy(app)

Tools = Tools()
Git = Git(Github)
Content = Content()
Section = Section()

from app import views, models