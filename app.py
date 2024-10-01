"""app.py: render and route to webpages"""
from flask import Flask, render_template

from socketserver import *

app = Flask(__name__)

@app.route('/')
def baseFile():
        return render_template("baseFile.html")

@app.route('/templates/')
def baseFile2():
    return render_template("baseFile2.html")

if __name__ == '__main__':
    app.run(debug=True)