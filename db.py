"""db.py: connect to Postgres database and create tables"""
import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# import environment variables from .env
load_dotenv()

# create the flask application with the same name as the file
app = Flask(__name__)

# tell flask which database you want to connect to. pulls values from .env
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('db_owner')}:{os.getenv('db_pass')}@localhost/{os.getenv('db_name')}"

# flask-sqlalchemy instance; used for all database interactions
db = SQLAlchemy(app)
