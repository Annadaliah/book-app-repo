"""app.py: render and route to webpages"""
from flask import render_template

from server import *

@app.route('/')
def login():
    
    return render_template("loginpage.html")

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)

