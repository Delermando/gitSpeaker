from flask import render_template
from flask import Markup
import base64
from app import *
@app.route("/")
def index():
    var = Tools.getEnviromentVar()
    #fileContent = getFileGetContent(var['GITSPEAKER_GH_REPOSITORYNAME'], var['GITSPEAKER_GH_FIRSTFILENAME'])
    #    return base64.b64decode(gitFile.content)

    user = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
    repository = Git.getRepository(user, var['GITSPEAKER_GH_REPOSITORYNAME'])
    dirContent = Git.getDirContentFromRepository(repository, '/')
    print(base64.b64decode(dirContent[6].content))


    formatedContent = formatFileContent(
        base64.b64decode(dirContent[6].content), 
        base64.b64decode(dirContent[6].name), 
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