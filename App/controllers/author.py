from App.models import Author
from App.database import db
#test commit
def create_author(name, dob, qualifications):
    new_author = Author(name=name, dob=dob, qualifications=qualifications)
    db.session.add(new_author)
    db.session.commit()
    return new_author

def get_author(id):
    return Author.query.get(id)

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

def get_author_by_name(name):
    print(name)
    authors = Author.query.filter_by(name=name)
    authors = [author for author in authors]
    # this code should be in a different method
    if not authors:
        new_author = create_author(name=name, dob=None, qualifications=None)
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
    