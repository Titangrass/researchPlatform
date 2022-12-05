from App.database import db
from .author import *
from .author_publication import *

AuthorPublication = db.Table(
    "authorpublication",
    db.Column("authpub_id", db.Integer, primary_key=True),
    #authpub_id = db.Column(db.Integer, primary_key=True)
    db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
    db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True),
    #authors = db.relationship('Author', backref='authorpublication', lazy=True),
    #publications = db.relationship('Publication', backref='authorpublication', lazy=True),
    #db.Column("auth_no", db.Integer)   
)

"""CoAuthorPublication = db.Table(
    "coauthorpublication",
    db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
    db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
)"""

