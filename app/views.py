from flask import render_template
from flask import Markup
from app import app
from github import Github
import base64
import os


@app.route("/")
def index():
    fileContent = getFileGetContent(os.environ.get('GITSPEAKER_GH_REPOSITORYNAME'), 'MarkNotUsedObejctsInFunction.py')
    formatedContent = formatFileContent('MarkNotUsedObejctsInFunction.py', fileContent)

    return render_template('index.html', content = Markup( formatedContent ))



def getFileGetContent(repositoryName, filename):
    github = Github(os.environ.get('GITSPEAKER_GH_USERNAME'), os.environ.get('GITSPEAKER_GH_PASSWORD'))
    user = github.get_user()
    repository = user.get_repo( repositoryName )
    gitFile = repository.get_contents( filename )
    return base64.b64decode(gitFile.content)



def groupRows( rows, rowsNumber, contentRowsNumber):
    groups = []
    group = ''

    if contentRowsNumber <= rowsNumber:
        contentRange = [0]
    else:
        contentRange = range(0, rowsNumber)

    for time in contentRange:
        for row in rows[ time : time + rowsNumber]:
            group += row + '\n'
        groups.append(group)
        group = ''
    
    return groups




def formatFileContent(filename, content):
    extension = filename.split('.')[1]
    if(extension == 'md'):
        pattern = getFormatPatterByFileExtension(extension)
        contentGroups = groupRows(content.splitlines(), 10, content.count('\n'))
        formatedContent = createSection(contentGroups, pattern)
    else:
        pattern = getFormatPatterByFileExtension(extension)
        contentGroups = groupRows(content.splitlines(), 19, content.count('\n'))
        formatedContent = createSection(contentGroups, pattern)
    return formatedContent


def getFormatPatterByFileExtension( fileExtension ):
    markdown = "<section data-markdown>%s</section>"
    code = "<section><pre><code>%s</code></pre></section>"
    if fileExtension == 'md':
        return markdown
    else:
        return code

def createSection(content, sectionPattner):
    html = ''
    print(type(content))
    print(len(content))

    for slide in content:
        html += sectionPattner % slide
        

    if len(content) > 1:
        html = "<section>%s</section>" % html

    print(html)
    return html
