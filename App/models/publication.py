from App.database import db
from .author import *
from .author_publication import *

# AuthorPublication = db.Table(
#     "authorpublication",
#     db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
#     db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
# )

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String)
    title = db.Column(db.String(120), nullable=False, unique=True)
    year = db.Column(db.String)
    doi = db.Column(db.String)
    authors = db.relationship("Author", secondary=AuthorPublication, lazy=True, backref=db.backref('publication', lazy=True))
    #authors = db.relationship(Author, secondary=AuthorPublication, backref='publication')

    def __init__(self, publisher, title, year, doi, authors):
        self.publisher = publisher
        self.title = title
        self.year = year
        self.doi = doi
        # self.authors.append(authors)
        # [self.authors.append(author) for author in authors]
        self.authors.extend(authors)

        #if coauthors:
            #self.coauthors.extend(coauthors)
    
    def toJSON(self):
        return{
            "id": self.id,
            "publisher": self.publisher,
            "title": self.title,
            "year": self.year,
            "doi": self.doi,
            "authors": [author.toJSON() for author in self.authors]
            #"coauthors": [coauthor.toJSON() for coauthor in self.coauthors]
        }
