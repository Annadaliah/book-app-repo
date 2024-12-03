from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, select

from db.server import app
from db.server import db
from flask import Flask

from db.schema.post import Post
from db.schema.user import User
from db.schema.book import Book

# Home route (for non-logged-in users)
@app.route('/', methods=['GET', 'POST'])
def home():
    # Select all books
    stmt = select(Book)
    all_books = db.session.execute(stmt)

    return render_template('signup.html')

# Signup route
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        query = insert(User).values(request.form)

        db.session.execute(query)
        db.session.commit()

        return redirect(url_for("loginpage"))

    return render_template('signup.html')

# Logged-in Home route (for users who are logged in)
@app.route('/LoggedInHome', methods=['GET', 'POST'])
def loggedInHome():
    # Select all books
    stmt = select(Book)
    all_books = db.session.execute(stmt)

    return render_template('LoggedInHome.html', books=all_books)

# Create post route
@app.route('/createpost', methods=['GET','POST'])
def createpost():
    if request.method == 'POST':
        query = insert(Post).values(request.form)

        db.session.execute(query)
        db.session.commit()

        return redirect(url_for("loggedInHome"))

    return render_template('createpost.html')

# Posts route (shows all posts)
@app.route('/posts')
def posts():
    # Select all posts
    stmt = select(Post)
    all_posts = db.session.execute(stmt)

    return render_template('posts.html', posts=all_posts)

# Login page route
@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    user_error_msg = ""
    if request.method == 'POST':
        if "Email" in request.form and "Password" in request.form:
            stmt = select(User.Password).where(User.Email == request.form['Email'])
            user = db.session.execute(stmt).fetchone()

            if user and user[0] == request.form['Password']:
                return redirect(url_for('loggedInHome'))
            else:
                user_error_msg = "Invalid credentials :("
                return render_template('loginpage.html', error=user_error_msg)

    return render_template('loginpage.html', error=user_error_msg)

# Delete post route
@app.route('/delete_post', methods=['POST'])
def delete_post():
    post_id = request.form['PostID']
    post_to_delete = Post.query.filter_by(PostID=post_id).first()

    # Try to delete the post associated with the given PostID
    try:
        if post_to_delete:
            db.session.delete(post_to_delete)
            db.session.commit()
            print("Post deleted successfully")
        else:
            print("Post not found")
    except Exception as error:
        db.session.rollback()  # Rollback in case of any error
        print(f"Error deleting post: {error}")

    return redirect(url_for('posts'))

# Edit post route
@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
def editpost(post_id):
    post = Post.query.get(post_id)

    if request.method == 'POST':
        # Update post fields
        post.BookName = request.form['BookName']
        post.Author = request.form['Author']
        post.Post = request.form['Post']

        db.session.commit()  # Save changes to database

        return redirect(url_for('posts'))  # Redirect back to posts page

    return render_template('editpost.html', post=post)  # Pass the post object to the template

# Application factory function
def create_app():
    app = Flask(__name__)

    # Set up configuration for the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/test_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    return app

if __name__ == '__main__':
    app.run(debug=True)