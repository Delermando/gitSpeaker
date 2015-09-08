from flask import Flask
from core import *

app = Flask(__name__)
Tools = Tools()
Git = Git()
Content = Content()
Section = Section()

from app import views