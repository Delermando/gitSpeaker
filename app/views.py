from flask import render_template
from flask import Markup
import base64
from app import *
@app.route("/")
def index():
    var = Tools.getEnviromentVar()
    user = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
    repository = Git.getRepository(user, var['GITSPEAKER_GH_REPOSITORYNAME'])
    dirContent = Git.getDirContentFromRepository(repository, '/')

    formatedContent = formatFileContent(
        dirContent[6].name, 
        base64.b64decode(dirContent[6].content), 
        int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), 
        int(var['GITSPEAKER_GH_CODELINESNUMBER'])
    )

    return render_template('index.html', content = Markup( formatedContent ))


def formatFileContent(filename, content, markdownLinesNumber, codeLinesNumber):
    extension = Tools.getFileExtension(filename)
    if(extension == 'md'):
        numberOfLines = markdownLinesNumber 
    else:
        numberOfLines = codeLinesNumber

    contentGroups = Content.rows(content.splitlines(), numberOfLines, content.count('\n'))
    return Section.set(contentGroups, Section.getPatter(extension))