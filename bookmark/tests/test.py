import pytest

from app import create_app
from tests.models import Base, User, Post, Book
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.server import get_db  # Adjust based on where your session creation is
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from db.server import db



@pytest.fixture
def app():
    # Use the app factory to create a testing app
    app = create_app(config_name='testing')
    
    # Create tables in the in-memory database
    with app.app_context():
        db.create_all()  # Create all tables for the test
        # Add a test user
        user = User(Email="test@example.com", Password="password")
        db.session.add(user)
        db.session.commit()

    yield app

    # Teardown: Drop the database after the test
    with app.app_context():
        db.drop_all()



# Define a fixture for the app and db session
@pytest.fixture
def app_and_db():
    # Create a Flask app instance
    app = create_app()

    # Set up a temporary database for testing
    DATABASE_URL = 'postgresql://postgres:Macrikel3!@localhost/postgres'  # Use a test database
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create the database tables for testing
    Base.metadata.create_all(bind=engine)

    # Create a session for the test
    db_session = Session()

    # Provide the app and db session to the test function
    yield app, db_session

    # Clean up after test: close the session and drop tables
    db_session.close()
    Base.metadata.drop_all(bind=engine)



# Test deleting a post
def test_delete_post(app_and_db):
    app, db_session = app_and_db

    # Insert a user to associate with the post (UserID)
    user = User(FirstName='Calista', LastName='Phippen', Email='calista.phippen1@marist.edu', Password='mypassword')
    db_session.add(user)
    db_session.commit()

    # Insert a post to delete (associating UserID)
    post_data = {
        'BookName': 'To Kill a Mockingbird',
        'Author': 'Harper Lee',
        'Post': 'A classic novel.',
        'UserID': user.UserID  # Associate the post with the user
    }
    post = Post(**post_data)
    db_session.add(post)
    db_session.commit()

    post_id = post.PostID

    # Simulate POST request to delete the post
    with app.test_client() as client:
        response = client.post('/delete_post', data={'PostID': post_id})
        assert response.status_code == 302  # Should redirect back to posts page

        # Verify the post was deleted
        deleted_post = db_session.query(Post).filter_by(PostID=post_id).first()
        assert deleted_post is None


# Test editing a post
def test_edit_post(app_and_db):
    app, db_session = app_and_db

    # Insert a user to associate with the post (UserID)
    user = User(FirstName='Calista', LastName='Phippen', Email='calista.phippen1@marist.edu', Password='mypassword')
    db_session.add(user)
    db_session.commit()

    # Insert a post to edit (associating UserID)
    post_data = {
        'BookName': '1984',
        'Author': 'George Orwell',
        'Post': 'A dystopian novel.',
        'UserID': user.UserID  # Ensure this is passed to create a post
    }
    post = Post(**post_data)
    db_session.add(post)
    db_session.commit()

    post_id = post.PostID  # Get the post ID

    # Simulate POST request to edit the post
    updated_post_data = {
        'BookName': 'Animal Farm',
        'Author': 'George Orwell',
        'Post': 'A novel about farm animals.',
        'UserID': user.UserID  # Ensure UserID is included
    }
    with app.test_client() as client:
        response = client.post(f'/editpost/{post_id}', data=updated_post_data)
        assert response.status_code == 302  # Should redirect to posts page

        # Verify the post was updated
        updated_post = db_session.query(Post).filter_by(PostID=post_id).first()
        assert updated_post.BookName == 'Animal Farm'
        assert updated_post.Author == 'George Orwell'


# Test missing fields on signup
def test_signup_no_firstname(app_and_db):
    app, db_session = app_and_db

    signup_data = {
        'LastName': 'Phippen',
        'Email': 'calista.phippen1@marist.edu',
        'Password': 'mypassword'
    }
    with app.test_client() as client:
        response = client.post('/signup', data=signup_data)
        assert response.status_code == 400  # Expect a 400 for missing field
        assert b"First Name is required" in response.data


def test_signup_no_lastname(app_and_db):
    app, db_session = app_and_db

    signup_data = {
        'FirstName': 'Calista',
        'Email': 'calista.phippen1@marist.edu',
        'Password': 'mypassword'
    }
    with app.test_client() as client:
        response = client.post('/signup', data=signup_data)
        assert response.status_code == 400  # Expect a 400 for missing field
        assert b"Last Name is required" in response.data


def test_signup_no_email(app_and_db):
    app, db_session = app_and_db

    signup_data = {
        'FirstName': 'Calista',
        'LastName': 'Phippen',
        'Password': 'mypassword'
    }
    with app.test_client() as client:
        response = client.post('/signup', data=signup_data)
        assert response.status_code == 400  # Expect a 400 for missing field
        assert b"Email is required" in response.data


def test_signup_no_password(app_and_db):
    app, db_session = app_and_db

    signup_data = {
        'FirstName': 'Calista',
        'LastName': 'Phippen',
        'Email': 'calista.phippen1@marist.edu'
    }
    with app.test_client() as client:
        response = client.post('/signup', data=signup_data)
        assert response.status_code == 400  # Expect a 400 for missing field
        assert b"Password is required" in response.data

@pytest.fixture
def sample_signup_input():
    return {'FirstName': 'Rian', 
            'LastName': 'Dickman', 
            'Email': 'rian@rian.com', 
            'Password': 'mypassword'
            }

# Test wrong credentials on login
def test_login_wrong_email(app_and_db, sample_signup_input):
    app, db_session = app_and_db

    user = User(**sample_signup_input)
    db_session.add(user)
    db_session.commit()

    with app.test_client() as client:
        response = client.post('/loginpage', data={'Email': 'wrong.email@example.com', 'Password': sample_signup_input['Password']})
        assert response.status_code == 200
        assert b"Invalid credentials" in response.data


def test_login_wrong_password(app_and_db, sample_signup_input):
    app, db_session = app_and_db

    user = User(**sample_signup_input)
    db_session.add(user)
    db_session.commit()

    with app.test_client() as client:
        response = client.post('/loginpage', data={'Email': sample_signup_input['Email'], 'Password': 'wrongpassword'})
        assert response.status_code == 200
        assert b"Invalid credentials" in response.data


def test_login_no_email(app_and_db):
    app, db_session = app_and_db

    with app.test_client() as client:
        response = client.post('/loginpage', data={'Email': '', 'Password': 'mypassword'})
        assert response.status_code == 200
        assert b"Email is required" in response.data


def test_login_no_password(app_and_db):
    app, db_session = app_and_db

    with app.test_client() as client:
        response = client.post('/loginpage', data={'Email': 'calista.phippen1@marist.edu', 'Password': ''})
        assert response.status_code == 200
        assert b"Password is required" in response.data
