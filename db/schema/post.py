from db.server import db

class Post(db.Model):
    __tablename__ = 'Posts'
    TableID = db.Column(db.Integer,primary_key=True, autoincrement=True)
    #column 1 will be user ID
    UserID = db.Column(db.Integer,primary_key=True, autoincrement=False)
    #column 2 will be the book they're posting about - max length is 40 characters
    BookName = db.Column(db.String(40))
    #column 3 will be the author - max length 40 characters (not required)
    Author = db.Column(db.String(40))
    #column 4 will be the actual post - no limit on charactes
    Post = db.Column(db.String)

    # Posts = db.relationship('Users', secondary = 'UserPost', back_populates = "Users")
    def __init__(self):

        self.BookName = self.BookName
        self.Author = self.Author
        self.Post = self.Post
        

    def __repr__(self):
        # add text to the f-string
        return f"""
            "User: {self.UserID},
             Book: {self.BookName},
             Author: {self.Author},
             Post: {self.Post}
        """
    
    def __repr__(self):
        return self.__repr__()