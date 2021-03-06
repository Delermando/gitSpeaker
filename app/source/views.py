from flask import render_template
from flask import Markup
import base64
from app import *
from app import models
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
    ignorelist = Tools.getIgnoreList('ignorelist.json')
    #GitSpeaker.saveUrlRepo(path)

    if var['GITSPEAKER_GH_ENVIRONMENT'] == 'prod':
        gitFiles = Git.getContents(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], urlParams['path'], 'master', ignorelist)
        response = GitSpeaker.getWrapperFileContents(gitFiles)
    else:
        fileList = Tools.getLocalFileList(path)
        filesContents = []
        for flPath in fileList:
            filesContents.append({'name':flPath, 'contents': Tools.getLocalContent(flPath)})
        response = GitSpeaker.getWrapperLocalFileContents(filesContents,int(var['GITSPEAKER_GH_MARKDOWNLINESNUMBER']), int(var['GITSPEAKER_GH_CODELINESNUMBER']))
    return render_template('slide.html', content = response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def slide(path):
    var = Tools.getEnviromentVar()
    ignorelist = Tools.getIgnoreList('ignorelist.json')
    urlParams = Git.extractUserRepoInfo(path)
    #GitSpeaker.saveUrlRepo(path)

    if var['GITSPEAKER_GH_ENVIRONMENT'] == 'prod':
        gitFiles = Git.getContents(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], urlParams['path'], 'master', ignorelist)
        print(gitFiles)
        response = GitSpeaker.getFileContents(gitFiles)     
    else:
        fileList = Tools.getLocalFileList(path)
        filesContents = []
        for flPath in fileList:
            filesContents.append({'name':flPath, 'contents': Tools.getLocalContent(flPath)})
        response = GitSpeaker.getLocalFileContents(filesContents)
    return render_template('slide.html', content = response)

