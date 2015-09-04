from flask import render_template
from app import app
from github import Github
import base64

@app.route("/")
def index():
    content = gitFileGetContent('gitSpeaker', 'server.py')
    return render_template('index.html', content = content)


def gitFileGetContent(repository, filename):
    github = Github('delermando', 'Aslam1618033989')
    user = github.get_user()
    repository = user.get_repo( repository )
    gitFile = repository.get_contents( filename )
    return base64.b64decode(gitFile.content)
