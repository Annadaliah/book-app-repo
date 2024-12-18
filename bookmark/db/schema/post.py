from db.server import db

class Post(db.Model):
    __tablename__ = 'Post'  # Ensure the table name matches your database schema
    PostID = db.Column(db.Integer, autoincrement = True, primary_key=True)  # Primary key
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