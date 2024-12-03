from db.server import db 

 

class Book(db.Model): 

__tablename__ = 'Book' 

BookID = db.Column(db.Integer, autoincrement=True,primary_key=True) 

#column 1 will be the book title - max length is 40 characters 

Title = db.Column(db.String(40)) 

#column 2 will be the author - max length is 40 characters 

Author = db.Column(db.String(40)) 

#column 3 will be the genre - max length 40 characters (not required) 

Genre = db.Column(db.String(40)) 

#column 4 will be the ISBN - string 

ISBN = db.Column(db.String) 

#column 5 will the publication date 

PubDate = db.Column(db.String) 

#column 6 is a description 

Desc = db.Column(db.String) 

#column 7 is for a cover image URL 

CoverImage = db.Column(db.String) 

#column 8 is for a user rating 

Rating = db.Column(db.Integer) 

 

# Posts = db.relationship('Users', secondary = 'UserPost', back_populates = "Users") 

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

return f"Book(Title= '{self.Title}', Author= {self.Author}, Genre= {self.Genre}, ISBN= {self.ISBN}, PubDate= {self.PubDate}, Desc = {self.Desc}, CoverImage= {self.CoverImage}, Rating= {self.Rating})" 

 

class Post(db.Model): 

__tablename__ = 'Post' # Ensure the table name matches your database schema 

PostID = db.Column(db.Integer, autoincrement = True, primary_key=True) # Primary key 

UserID = db.Column(db.Integer, nullable=False) 

BookName = db.Column(db.String(100), nullable=False) 

Author = db.Column(db.String(100), nullable=False) 

Post = db.Column(db.Text, nullable=False) 

 

def __repr__(self): 

return f"<Post {self.PostID}>" 

 

# Posts = db.relationship('Users', secondary = 'UserPost', back_populates = "Users") 

def __init__(self, UserID, BookName, Author, Post): 

 

self.UserID = UserID 

self.BookName = BookName 

self.Author = Author 

self.Post = Post 

def __repr__(self): 

return self.__repr__() 

 

class User(db.Model): 

__tablename__ = 'User' 

UserID = db.Column(db.Integer, autoincrement=True,primary_key=True) 

FirstName = db.Column(db.String(40)) 

LastName = db.Column(db.String(40)) 

Email = db.Column(db.String(40)) 

Password = db.Column(db.String(256)) 

 

def __init__(self, UserID, FirstName, LastName, Email, Password): 

self.UserID = UserID 

self.FirstName = FirstName 

self.LastName = LastName 

self.Email = Email 

self.Password = Password 

 

def __repr__(self): 

return f""" 

"FIRST NAME: {self.FirstName}, 

LAST NAME: {self.LastName}, 

EMAIL: {self.Email}, 

User ID: {self.UserID}, 

PASSWORD: {self.Password} 

""" 

def __repr__(self): 

return self.__repr__() 

 

 

class Post(db.Model): 

__tablename__ = 'posts' 

 

PostID = db.Column(db.Integer, primary_key=True) 

content = db.Column(db.String(500), nullable=False) 

 

def __init__(self, content): 

self.content = content 