#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World</hi>"

if __name__ == "__main__":
    app.run(debug=True, int(os.environ.get("PORT", 5000)))