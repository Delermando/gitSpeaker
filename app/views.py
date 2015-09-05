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
    contentGroups = groupRows(content.splitlines(), 10, content.count('\n'))
   
    #content = m.html(content,extensions=m.EXT_STRIKETHROUGH)
    #return render_template('index.html', content = Markup(content))
    contentGroups = createSection( contentGroups )
    return render_template('index.html', content = Markup(contentGroups))


def gitFileGetContent(repositoryName, filename):
    github = Github(os.environ.get('GITSPEAKER_GH_USERNAME'), os.environ.get('GITSPEAKER_GH_PASSWORD'))
    user = github.get_user()
    repository = user.get_repo( repositoryName )
    gitFile = repository.get_contents( filename )
    return base64.b64decode(gitFile.content)



def groupRows( rows, rowsNumber, contentRowsNumber):
    groups = []
    group = ''
    times = (contentRowsNumber/rowsNumber)
    if (contentRowsNumber % rowsNumber ) != 0:
        times += 1

    for time in range(0, contentRowsNumber, times):
        
        for row in rows[ time : time + rowsNumber]:
            group += row + '\n'
        groups.append(group)
        group = ''
    return groups


def createSection(content):
    html = ''
    for slide in content:
        html += "<section data-markdown>%s</section>" % slide

    return html



