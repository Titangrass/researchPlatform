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

"""
def getpublicationtree(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()
"""

def add_edge(graph, auth1, auth2, pub):
    
    if graph[auth1][auth2]:
        graph[auth1][auth2].append(pub) #check to see if there is a list of publications present
    else:
        graph[auth1][auth2] = [pub] #if there is no list, add the publication to the list
        
def print_graph(graph):
    
    n = len(graph)
    for i in range(n):
        print(f'\t{i+1}\t', end=' |')
    for i in range(n):
        print(f'\n {i+1}', end=' |') 
    for j in range(n):
        print(graph[i][j], end=' |')
        
        
def build_graph(authors):
    pubs = Publication.query.all()
    num = len(authors)
    graph = [[ None for i in range(num)] for j in range(num)]
    for pub in pubs:
        for a1 in pub.authors:
            for a2 in pub.authors:
                add_edge(graph, authors.index[a1], authors.index[a2], pub)
    return graph

def get_pubtree(author):
    
    authors = Authors.query.all()
    num = len(authors)
    graph = build_graph(authors)
    print_graph(graph)
    a_set = {author}
    stack = [author]
    while stack:
        
        auth = stack.pop()
        author_no = authors.index(auth)
        print(f"{auth.id} worked with authors", end=":")
        row = graph[author_no]
        for i in range(num):
            if row[i] != None and not (authors[i] in a_set):
                stack.append(authors[i])
                print(f'{authors[i].id}', end =",")
                a_set.add(authors[i])
        print('\n')
        all_pubs = set()
        for a in a_set:
            for p in a.publications:
                all_pubs.add(p)
        print(all_pubs)
    