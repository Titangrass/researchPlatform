from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .author import *
from .author_publication import *

#class User(db.Model):
class User(Author):
    user_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    username =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, firstName, lastName, dob, email, qualifications):
        #self.author_id = author_id
        super().__init__(firstName, lastName, dob, email, qualifications)
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return{
            'user_id': self.user_id,
            'author_id': self.author_id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

