from flask import render_template
from flask import Markup
import base64
from app import *

@app.route("/")
def apresentation():
    return render_template('apresentation.html')

@app.route('/wrapper/', defaults={'path': ''})
@app.route('/wrapper/<path:path>')
def wrapper(path):
    var = Tools.getEnviromentVar()
    #Run local, 
    var['GITSPEAKER_GH_FILECONTENT'] = open( 'app/mock/' + path).read().decode('utf-8')
    response = Markup(formatFileContent(var['GITSPEAKER_GH_FIRSTFILENAME'], var['GITSPEAKER_GH_FILECONTENT'], int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))

#    urlParams = Git.extractUserRepoInfo(path)
#    branchName = 'master'
#    response = ''

#    git = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
#    user = Git.getSearcUser(git, urlParams['user'] )
#    repository = Git.getRepository(user , urlParams['repository'])
#    branch = Git.getBranch( repository, branchName)
#    tree = Git.getTree(repository, branch.commit.sha, True)
#    fileDict = Git.extractFileListInfo(tree)
#    fl = Git.checkFile(fileDict, urlParams['path'])
#
    
#    if fl == 'blob':
#        gitFl = Git.getFileContent(repository, urlParams['path'])
#        response = Markup(formatFileContentWrapper(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))
#    elif fl == 'tree':
#        gitDir = Git.getDirContentFromRepository(repository, urlParams['path'])
#        for gitFl in gitDir:
#            response += Markup(formatFileContentWrapper(gitFl.name, base64.b64decode(gitFl.content), int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))
#    else:
#        response = 'Nao existe'

    
    return render_template('slide.html', content = response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def slide(path):
    var = Tools.getEnviromentVar()
    #Run local, 
    #var['GITSPEAKER_GH_FILECONTENT'] = open( 'app/mock/' + path).read().decode('utf-8')
    #response = Markup(formatFileContent(var['GITSPEAKER_GH_FIRSTFILENAME'], var['GITSPEAKER_GH_FILECONTENT'], int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ))

    urlParams = Git.extractUserRepoInfo(path)
    branchName = 'master'
    response = ''

    git = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
    user = Git.getSearcUser(git, urlParams['user'] )
    repository = Git.getRepository(user , urlParams['repository'])
    branch = Git.getBranch( repository, branchName)
    tree = Git.getTree(repository, branch.commit.sha, True)
    fileDict = Git.extractFileListInfo(tree)
    fl = Git.checkFile(fileDict, urlParams['path'])
    
    if fl == 'blob':
        gitFl = Git.getFileContent(repository, urlParams['path'])
        response = Markup(formatFileContent(gitFl.name, base64.b64decode(gitFl.content)).decode('utf-8'))
    elif fl == 'tree':
        gitDir = Git.getDirContentFromRepository(repository, urlParams['path'])
        for gitFl in gitDir:
            response += Markup(formatFileContent(gitFl.name, base64.b64decode(gitFl.content) ).decode('utf-8'))
    else:
        response = 'Nao existe'

    
    return render_template('slide.html', content = response)


def formatFileContentWrapper(filename, content, markdownLinesNumber, codeLinesNumber):
    extension = Tools.getFileExtension(filename)
    rows = content.splitlines()
    rowsLen = len(rows)
    if(extension == 'md'):
        contentGroups = Content.rowsMdFiles(rows, markdownLinesNumber, rowsLen)
    else:
        contentGroups = Content.rowsCodeFiles(rowsLen, codeLinesNumber, rowsLen)
    return Section.set(contentGroups, Section.getPatter(extension))

def formatFileContent(filename, content):
    extension = Tools.getFileExtension(filename)
    return Section.setWrapper(content, Section.getPatter(extension))