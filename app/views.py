from flask import render_template
from flask import Markup
import base64
from app import *
from gitSpeaker import GitSpeaker

GitSpeaker = GitSpeaker()

@app.route("/")
def apresentation():
    return render_template('apresentation.html')

@app.route('/wrapper/', defaults={'path': ''})
@app.route('/wrapper/<path:path>')
def wrapper(path):
    var = Tools.getEnviromentVar()
    urlParams = Git.extractUserRepoInfo(path)
    print(urlParams)
    
    if var['GITSPEAKER_GH_ENVIRONMENT'] == 'prod':
        gitFiles = Git.getContents(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], 'master')
        response = GitSpeaker.getFileContents(gitFiles)
    else:
        fileList = Tools.getLocalFileList(path, '*')
        filesContents = []

        for flPath in fileList:
            filesContents.append({'name':flPath, 'contents': Tools.getLocalContent(flPath)})

        response = GitSpeaker.getLocalFileContents(filesContents,int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']))

        #response = Markup(GitSpeaker.formatFileContentWrapper(var['GITSPEAKER_GH_FIRSTFILENAME'], var['GITSPEAKER_GH_FILECONTENT'], int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']) ).decode('utf-8'))
    
    return render_template('slide.html', content = response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def slide(path):
    var = Tools.getEnviromentVar()
    
    if var['GITSPEAKER_GH_ENVIRONMENT'] == 'prod':
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
    else:
        var['GITSPEAKER_GH_FILECONTENT'] = open( 'app/mock/' + path).read().decode('utf-8')
        response = Markup(GitSpeaker.formatFileContent(var['GITSPEAKER_GH_FIRSTFILENAME'], var['GITSPEAKER_GH_FILECONTENT'] ))
    
    return render_template('slide.html', content = response)

