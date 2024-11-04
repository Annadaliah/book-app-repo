"""db.py: connect to Postgres database and create tables"""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from db.sql import queries

# import environment variables from .env
load_dotenv()

db_name: str = os.getenv('db_name')
db_owner: str = os.getenv('db_owner')
db_pass: str = os.getenv('db_pass')
db_uri: str = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

# create the flask application & connect to db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)

# this import is here because we need to initialize db before importing it into
# the classes
from db.schema.user import User


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

    # run queries to remove data from tables
    for key, value in queries.items():
        db.session.execute(text(value))
        db.session.commit()



