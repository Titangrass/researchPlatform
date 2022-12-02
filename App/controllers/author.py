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

# search that retrieves all publications of the author 
# as well as the publications of any co-authors of the author, 
# and the co-authors of their co-authors etc.

# getpublicationtree needs 
# author root  
# all publications of this author 
# and any publication of any coauthor associated wih this author
# # functionality in get_publications()
# we have basically a mesh network of authors and publications 
# each of which may or may not be connected to each other and
# we need to find the path that links all coauthours to the author in the search

# search for author done by get_author(id)
# get publications of this author done by get_publications()
# get publication has a list of authors 
# for all authors of current Publication 
#     get their publications and log each subsequent publication's authors 

# need to store:
# all authors 
# all publications 

# a binary tree where each node is an author and each has a publication/s
# we do a bfs that looks at every node and tests 
# if it has a publication in common with the current list of authors 
# and we do this search until the list of authors is exhausted