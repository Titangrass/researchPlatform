from App.models import Author
from App.database import db

def create_author(firstName, lastName, dob, email, qualifications):
    new_author = Author(firstName=firstName, lastName=lastName, dob=dob, email=email, qualifications=qualifications)
    db.session.add(new_author)
    db.session.commit()
    return new_author

def get_author(id):
    return Author.query.get(id)

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not authors:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

def get_author_by_name(firstName, lastName):
    print(firstName + " " + lastName)
    authors = Author.query.filter_by(firstName=firstName, lastName=lastName)
    authors = [author for author in authors]
    # this code should be in a different method
    if not authors:
        new_author = create_author(firstName=firstName, lastName=lastName, dob=None, email=None, qualifications=None)
        authors = [new_author]
        return authors
    return authors

def get_author_publications(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()

def getpublicationtree(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()
    