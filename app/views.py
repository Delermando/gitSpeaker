from gitSpeaker import GitSpeaker
from app import *

# from flask import Markup
# import base64


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

# @app.route('/wrapper/', defaults={'path': ''})
# @app.route('/wrapper/<path:path>')
# def wrapper(path):
