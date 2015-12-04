from flask import render_template
from gitSpeaker import GitSpeaker
from app import *

# from flask import Markup


GitSpeaker = GitSpeaker()
var = Tools.getEnviromentVar()
ignorelist = Tools.getIgnoreList('ignorelist.json')


@app.route("/")
def apresentation():
    return render_template('apresentation.html')


@app.route('/', defaults={'path': ''},  methods=['GET'])
@app.route('/<path:path>',  methods=['GET'])
def slide(path):
    urlParams = Git.extractUserRepoInfo(path)
    GitSpeaker.saveUrlRepo(path)
    gitFiles = Git.getFileList(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], urlParams['path'], 'master', ignorelist)
    return GitSpeaker.returnFileList(200, "", gitFiles)


@app.route('/v1/list/', defaults={'path': ''},  methods=['GET'])
@app.route('/v1/list/<path:path>',  methods=['GET'])
def fileList(path):
    urlParams = Git.extractUserRepoInfo(path)
    GitSpeaker.saveUrlRepo(path)
    gitFiles = Git.getFileList(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], urlParams['path'], 'master', ignorelist)
    return GitSpeaker.returnFileList(200, "", gitFiles)


@app.route('/v1/content/', defaults={'path': ''},  methods=['GET'])
@app.route('/v1/content/<path:path>',  methods=['GET'])
def fileContent(path):
    urlParams = Git.extractUserRepoInfo(path)
    gitContents = Git.getContent(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'], urlParams['user'], urlParams['repository'], urlParams['path'], 'master', ignorelist)
    content = GitSpeaker.getWrapperFileContents(gitContents)
    return GitSpeaker.returnFileContent(200, "", content)
