"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.post import Post
from db.schema.user import User
from db.schema.book import Book

from socketserver import *

@app.route('/', methods=['GET', 'POST'])
def home():
    with app.app_context():

        # select all posts
        stmt = select(Book)
        all_books = db.session.execute(stmt)

        return render_template('NotLoggedInHome.html')
    return render_template("NotLoggedInHome.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    print(request.method)
    if request.method == 'POST':
       
        for key, value in request.form.items():
             print(f'{key}: {value}')
        query = insert(User).values(request.form)

        with app.app_context():
                db.session.execute(query)
                db.session.commit()

        return redirect (url_for ("loginpage"))

    return render_template('signup.html')

@app.route('/LoggedInHome', methods=['GET', 'POST'])
def loggedInHome():
    with app.app_context():

        # select all posts
        stmt = select(Book)
        all_books = db.session.execute(stmt)

        return render_template('LoggedInHome.html', books=all_books)
    return render_template("NotLoggedInHome.html")

@app.route('/createpost', methods=['GET','POST'])
def createpost():
    if request.method == 'POST':
       
        query = insert(Post).values(request.form)

        with app.app_context():
                db.session.execute(query)
                db.session.commit()

        return redirect (url_for ("loggedInHome"))

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
    user_error_msg = ""
    if request.method == 'POST':

        if "Email" in request.form and "Password" in request.form:
        
            stmt = select(User.Password).where(User.Email == request.form['Email'])
            user = db.session.execute(stmt).fetchone()
            print(user)
            print(request.form['Password'])

            if user[0] == request.form['Password']:
                return redirect(url_for('loggedInHome'))
        
            else: 
                user_error_msg = "invalid credentials :("
                return render_template('loginpage.html', error = user_error_msg)

    return render_template('loginpage.html', error = user_error_msg)

@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form['PostID']
    post_to_delete = Post.query.filter_by(PostID=post_id).first()
    
    # Try to delete the post associated with the given UserID
    try:
        # Query to find and delete the post
        post_to_delete = Post.query.filter_by(PostID=post_id).first()
        if post_to_delete:
            db.session.delete(post_to_delete)
            db.session.commit()
            print("Post deleted successfully")
        else:
            print("Post not found")
    except Exception as error:
        db.session.rollback()  # Rollback in case of any error
        print(f"Error deleting post: {error}")
    
    return redirect(url_for('home'))

@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
def editpost(post_id):
    post = Post.query.get(post_id)
    
    if request.method == 'POST':
        # Handle form submission to update the post
        post.BookName = request.form['BookName']
        post.Author = request.form['Author']
        post.Post = request.form['Post']
        
        db.session.commit()  # Save changes to database
        
        return redirect(url_for('posts'))  # Redirect back to posts page (or wherever you want)

    return render_template('editpost.html', post=post)  # Pass the post object to the template


if __name__ == '__main__':
    app.run(debug=True)

