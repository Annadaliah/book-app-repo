"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.post import Post
from db.schema.user import User
from db.schema.books import Book

from socketserver import *

@app.route('/', methods=['GET', 'POST'])
def home():
    with app.app_context():

        # select all posts
        stmt = select(Book)
        all_books = db.session.execute(stmt)

        return render_template('home.html', books=all_books)
    return render_template("home.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
     if request.method == 'POST':
       
        query = insert(User).values(request.form)

        with app.app_context():
                db.session.execute(query)
                db.session.commit()

        return redirect (url_for ("loginpage"))


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

@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    
    if request.method == 'POST':

        if "Email" in request.form and "Password" in request.form:
        
            stmt = select(User.Password).where(User.Email == request.form['Email'])
            user = db.session.execute(stmt).fetchone()
            print(user)
            print(request.form['Password'])

            if user[0] == request.form['Password']:
                return redirect(url_for('oklogin'))
        
            else: 
                return redirect(url_for('home2'))   
             
    return render_template('loginpage.html')



if __name__ == '__main__':
    app.run(debug=True)

