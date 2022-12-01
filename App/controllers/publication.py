from App.models import Publication
from App.database import db

def create_publication(publisher, title, year, doi, authors):
    new_publication = Publication(publisher, title, year, doi, authors)
    db.session.add(new_publication)
    db.session.commit()
    return new_publication

def get_publication(id):
    return Publication.query.get(id)

def get_all_publications():
    return Publication.query.all()

def get_all_publications_json():
    publications = Publication.query.all()
    if not publications:
        return []
    publications = [publication.toJSON() for publication in publications]
    return publications