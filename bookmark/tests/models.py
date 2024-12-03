from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create the base class for your models
Base = declarative_base()

# Database engine and session setup
DATABASE_URL = 'postgresql://username:password@localhost/dbname'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session function to provide a session in views or other functions
def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()

class Post(Base):
    __tablename__ = 'Post'
    PostID = Column(Integer, autoincrement=True, primary_key=True)
    UserID = Column(Integer, nullable=False)
    BookName = Column(String(100), nullable=False)
    Author = Column(String(100), nullable=False)
    Post = Column(Text, nullable=False)

    def __init__(self, UserID, BookName, Author, Post):
        self.UserID = UserID
        self.BookName = BookName
        self.Author = Author
        self.Post = Post

    def __repr__(self):
        return f"<Post {self.PostID}>"

class User(Base):
    __tablename__ = 'User'
    UserID = Column(Integer, autoincrement=True, primary_key=True)
    FirstName = Column(String(40))
    LastName = Column(String(40))
    Email = Column(String(40))
    Password = Column(String(256))

    def __init__(self, FirstName, LastName, Email, Password):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Password = Password

    def __repr__(self):
        return f"""User(FirstName='{self.FirstName}', LastName='{self.LastName}', 
                    Email='{self.Email}', UserID={self.UserID}, Password='{self.Password}')"""

class Book(Base):
    __tablename__ = 'Book'
    BookID = Column(Integer, autoincrement=True, primary_key=True)
    Title = Column(String(40))
    Author = Column(String(40))
    Genre = Column(String(40))
    ISBN = Column(String)
    PubDate = Column(String)
    Desc = Column(String)
    CoverImage = Column(String)
    Rating = Column(Integer)

    def __init__(self, Title, Author, Genre, ISBN, PubDate, Desc, CoverImage, Rating):
        self.Title = Title
        self.Author = Author
        self.Genre = Genre
        self.ISBN = ISBN
        self.PubDate = PubDate
        self.Desc = Desc
        self.CoverImage = CoverImage
        self.Rating = Rating

    def __repr__(self):
        return f"Book(Title='{self.Title}', Author='{self.Author}', Genre='{self.Genre}', ISBN='{self.ISBN}', " \
               f"PubDate='{self.PubDate}', Desc='{self.Desc}', CoverImage='{self.CoverImage}', Rating={self.Rating})"

