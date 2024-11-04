"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.post import Post

from socketserver import *

@app.route('/')
def baseFile():
        return render_template("baseFile.html")

@app.route('/templates/')
def baseFile2():
    return render_template("baseFile2.html")

@app.route('/home')
def Home():
     return render_template('home.html')

@app.route('/home2', methods=['GET', 'POST'])
def Home2():
     
# """      if request.method == "POST":

#           with app.app_context():

#                query = insert(Post).values(request.form)

#                with app.app_context():
#                     db.session.execute(query)
#                     db.session.commit()
          
#           return render_template('home2.html') """
     return render_template("home2.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
     if request.method == 'POST':
       
        query = insert(User).values(request.form)

        with app.app_context():
                db.session.execute(query)
                db.session.commit()

        return redirect (url_for ("signup"))


     return render_template('signup.html')

@app.route('/createpost', methods=['GET','POST'])
def createpost():
     if request.method == 'POST':
       
          query = insert(Post).values(request.form)

          with app.app_context():
                db.session.execute(query)
                db.session.commit()

          """ return redirect (url_for ('home2')) """

     return render_template('createpost.html')

@app.route('/posts')
def posts():
    with app.app_context():

        # select all posts
        stmt = select(Post)
        all_posts = db.session.execute(stmt)

        return render_template('posts.html', posts=all_posts)
    
    return render_template('posts.html')

if __name__ == '__main__':
    app.run(debug=True)