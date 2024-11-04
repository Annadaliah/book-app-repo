"""user.py: create a table named users"""
from db.server import db

class User(db.Model):
    __tablename__ = 'Users'
    TableID = db.Column(db.Integer, autoincrement=True)
    UserID = db.Column(db.String,primary_key=True)
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
    