from db.server import db

class Book(db.Model):
    __tablename__ = 'Books'
    TableID = db.Column(db.Integer, autoincrement=True)
    #column 1 will be the book title - max length is 40 characters
    Title = db.Column(db.String(40),primary_key=True)
    #column 2 will be the author - max length is 40 characters
    Author = db.Column(db.String(40))
    #column 3 will be the genre - max length 40 characters (not required)
    Genre = db.Column(db.String(40))
    #column 4 will be the ISBN - integer
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
        return self.__repr__()