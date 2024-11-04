"""app.py: render and route to webpages"""
from flask import Flask, render_template

from socketserver import *

app = Flask(__name__)

@app.route('/')
def login():
    
    return render_template("loginpage.html")

if __name__ == '__main__':
    app.run(debug=True)

