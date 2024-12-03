import os
import pytest

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app import create_app  # Import your app's creation function
from db import db_session   # Import your database session
from db.server import db
from tests.models import User
from tests.models import Post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests import create_app, db
from tests.models import User, Post, Book  

# contains table objects
Base = declarative_base()

# import environment variables from .env
load_dotenv()

db_name: str = os.getenv('db_name')
db_owner: str = os.getenv('db_owner')
db_pass: str = os.getenv('db_pass')
db_uri: str = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

# create db connection w/o Flask
# NOTE: creates new session for each test function


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(db_uri) 
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # create tables
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    yield session
    session.close()
    # drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_signup_input():
    return {'FirstName': 'Rian', 
            'LastName': 'Dickman', 
            'Email': 'rian@rian.com', 
            'Password': 'mypassword'
            }

@pytest.fixture
def app():
    app = create_app('testing')  # Use the 'testing' config for the app
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def db_session(app):
    # Setup a clean database session for each test
    db.create_all()
    yield db.session
    db.session.rollback()  # Rollback changes after each test
    db.session.remove()

@pytest.fixture
def app_and_db(app, db_session):
    return app, db_session

@pytest.fixture
def setup_test_data():
    # Create a test user
    user = User(Email="test@example.com", Password="password", FirstName="John", LastName="Doe")
    db.session.add(user)
    db.session.commit()  # Commit to get the UserID

    # Create a test post
    post = Post(UserID=user.UserID, BookName="Test Book", Author="Author Name", Post="Test post content")
    db.session.add(post)
    db.session.commit()  # Commit to save the post

    yield user, post  # Return user and post for use in tests

    # Clean up after tests
    db.session.remove()
    db.drop_all()