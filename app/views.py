from flask import render_template
from flask import Markup
import base64
from app import *

@app.route("/")
def apresentation():
    return render_template('apresentation.html')

@app.route('/get/', defaults={'path': ''})
@app.route('/get/<path:path>')
def slide(path):
    var = Tools.getEnviromentVar()
    var['GITSPEAKER_GH_FILECONTENT'] = open( 'app/mock/' + path).read().decode('utf-8')
    #urlParams = Git.extractUserRepoInfo(path)
    #branchName = 'master'
    #response = ''

    #git = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
    #user = Git.getSearcUser(git, urlParams['user'] )
    #repository = Git.getRepository(user , urlParams['repository'])
    #branch = Git.getBranch( repository, branchName)
    #tree = Git.getTree(repository, branch.commit.sha, True)
    #fileDict = Git.extractFileListInfo(tree)
    #fl = Git.checkFile(fileDict, urlParams['path'])

    response = Markup(formatFileContent(var['GITSPEAKER_GH_FIRSTFILENAME'], var['GITSPEAKER_GH_FILECONTENT'], int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))
    #if fl == 'blob':
    #    gitFl = Git.getFileContent(repository, urlParams['path'])
    #    response = Markup(formatFileContent(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))
    #elif fl == 'tree':
    #    gitDir = Git.getDirContentFromRepository(repository, urlParams['path'])
    #    for gitFl in gitDir:
    #        response += Markup(formatFileContent(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))
    #else:
    #    response = 'Nao existe'

    
    return render_template('slide.html', content = response)


def formatFileContent(filename, content, markdownLinesNumber, codeLinesNumber):
    extension = Tools.getFileExtension(filename)
    rows = content.splitlines()
    rowsLen = len(rows)
    if(extension == 'md'):
        contentGroups = Content.rowsMdFiles(rows, markdownLinesNumber, rowsLen)
    else:
        contentGroups = Content.rowsCodeFiles(rowsLen, codeLinesNumber, rowsLen)
    return Section.set(contentGroups, Section.getPatter(extension))