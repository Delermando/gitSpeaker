from flask import render_template, jsonify
from gitSpeaker import GitSpeaker
from app import *
import time

# from flask import Markup
# import base64
# from app import models


GitSpeaker = GitSpeaker()


@app.route("/")
def apresentation():
    return render_template('apresentation.html')


response = {
    "status_code": 200,
    "message": "",
    "data": {
        "page": 'teste'
    }
}


@app.route('/', defaults={'path': ''},  methods=['GET'])
@app.route('/<path:path>',  methods=['GET'])
def slide(path):
    time.sleep(5)
    return jsonify({"response": response})


# @app.route('/wrapper/', defaults={'path': ''})
# @app.route('/wrapper/<path:path>')
# def wrapper(path):
