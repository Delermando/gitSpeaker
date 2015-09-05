from flask import render_template
from flask import Markup
from app import app
from github import Github
import base64
import os
import misaka as m 

@app.route("/")
def index():
    content = gitFileGetContent(os.environ.get('GITSPEAKER_GH_REPOSITORYNAME'), os.environ.get('GITSPEAKER_GH_FIRSTFILENAME'))
    content = m.html(content,extensions=m.EXT_STRIKETHROUGH)
    return render_template('index.html', content = Markup(content))


def gitFileGetContent(repositoryName, filename):
    github = Github(os.environ.get('GITSPEAKER_GH_USERNAME'), os.environ.get('GITSPEAKER_GH_PASSWORD'))
    user = github.get_user()
    repository = user.get_repo( repositoryName )
    gitFile = repository.get_contents( filename )
    return base64.b64decode(gitFile.content)
