from flask import Flask
from core import *
from github import Github

app = Flask(__name__)
Tools = Tools()
Git = Git(Github)
Content = Content()
Section = Section()

from app import views