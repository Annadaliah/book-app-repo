"""db.py: connect to Postgres database and create tables"""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# db/server.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DATABASE_URL = 'postgresql://username:password@localhost/dbname'  # Adjust for your test environment

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is your get_db function
def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # or your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize the SQLAlchemy instance


# import environment variables from .env
load_dotenv()

db_name: str = os.getenv('db_name')
db_owner: str = os.getenv('db_owner')
db_pass: str = os.getenv('db_pass')
db_uri: str = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

# create the flask application & connect to db
app = Flask(__name__, 
            template_folder = os.path.join(os.getcwd(), 'templates'), 
            static_folder=os.path.join(os.getcwd(), 'static'))
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)

# import table to be created in postgres
from db.schema.post import Post
from db.schema.user import User
from db.schema.book import Book

# verify the db connection is successful
with app.app_context():
    # attempt to connect to db, print msgs if successful
    try:
        # run SQL query to verify connection (see how we use the db instance?)
        db.session.execute(text("SELECT 1"))
        print(f"\n\n----------- Connection successful!")
        print(f" * Connected to database: {os.getenv('db_name')}")
    # failed to connect to db, provide msgs & error
    except Exception as error:
        print(f"\n\n----------- Connection failed!")
        print(f" * Unable to connect to database: {os.getenv('db_name')}")
        print(f" * ERROR: {error}")

        
    
    # create all database tables
    db.create_all()
    db.session.commit()