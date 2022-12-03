from App.database import db
from datetime import *
from .author_publication import *

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    firstName =  db.Column(db.String, nullable=False)
    lastName =  db.Column(db.String, nullable=False)
    dob = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String)
    qualifications = db.Column(db.String(350), nullable=True)
    publications = db.relationship("Publication", secondary=AuthorPublication, viewonly=True)

    def __init__(self, firstName, lastName, dob, email, qualifications):
        self.firstName = firstName
        self.lastName = lastName
        if dob:
            self.dob = datetime.strptime(dob, "%d/%m/%Y")
        self.email = email
        if qualifications:
            self.qualifications = qualifications

    def get_publications(self):
        # return [publication.toJSON() for publication in self.publications]
        return [publication.toJSON() for publication in self.publications]

    def add_pub(self, publication, author_no ):
        pubs = []
        #pubs.append(publication)
        pubs.insert(author_no, publication)
        self.publications = pubs


    def toJSON(self):
        return{
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dob': self.dob,
            'email': self.email,
            'qualifications': self.qualifications,
        }

