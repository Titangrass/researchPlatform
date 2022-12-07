import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import *

from App.main import create_app
from App.database import create_db
from App.models import User, Author, Publication
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    create_publication,
    get_all_authors_json,
    create_author,
    create_publication,
    get_all_publications_json,
    get_author
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "Bob", "Moog", "05/08/2001", "bob@mail", "BSc. Computer Science")
        assert user.username == "bob"

    def test_user_toJSON(self):
        user = User("bob", "bobpass", "Bob", "Moog", "05/08/2001", "bob@mail", "BSc. Computer Science")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"user_id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password, "Bob", "Moog", "05/08/2001", "bob@mail", "BSc. Computer Science")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, "Bob", "Moog", "05/08/2001", "bob@mail", "BSc. Computer Science")
        assert user.check_password(password)

class AuthorUnitTests(unittest.TestCase):

    def test_new_author(self):
        #author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        author = Author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science")
        assert author.firstName == "Bob" and author.lastName == "Moog" and author.dob == datetime.strptime("05/08/2001", "%d/%m/%Y") and author.email == "bob@mail" and author.qualifications == "BSc. Computer Science"

    def test_author_toJSON(self):
        #author = Author("Bob Moog", "05/08/2001", "BSc. Computer Science")
        author = Author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science")
        author_json = author.toJSON()
        self.assertDictEqual(author_json, {
            "id": None,
            "firstName": "Bob",
            "lastName": "Moog",
            "email": "bob@mail",
            "dob": datetime.strptime("05/08/2001", "%d/%m/%Y"),
            "qualifications": "BSc. Computer Science"
        })

class PublicationUnitTests(unittest.TestCase):
    def test_new_publication(self):
        authors = []
        #coauthors = []
        author = Author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science")
        authors.append(author)
        #coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        #coauthors.append(coauthor)
        publication = Publication("Grandburgh", "Intro to Computer Science", "2018", "10.1080/02626667.2018.1560449", authors)
        assert (
            publication.publisher=="Grandburgh" 
            and publication.title=="Intro to Computer Science"
            and publication.year=="2018" 
            and publication.doi=="10.1080/02626667.2018.1560449" 
            and publication.authors==authors 
            #and publication.coauthors==coauthors
        )

    def test_publication_toJSON(self):
        authors = []
        #coauthors = []
        author = Author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science")
        authors.append(author)
        #coauthor = Author("Bob Dule", "06/09/2002", "BSc. Computer Engineering")
        #coauthors.append(coauthor)
        publication = Publication("Grandburgh", "Intro to Computer Science", "2018", "10.1080/02626667.2018.1560449", authors)
        publication_json = publication.toJSON()
        self.assertDictEqual(publication_json, {
            "id": None,
            "publisher": "Grandburgh",
            "title": "Intro to Computer Science",
            "year": "2018",
            "doi": "10.1080/02626667.2018.1560449",
            "authors": [author.toJSON() for author in authors],
            #"coauthors": [coauthor.toJSON() for coauthor in coauthors]
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):
    def test_authenticate(self):
        user = create_user("bob", "bobpass", "Bob", "Moog", "05/08/2001", "bob@mail", "BSc. Computer Science")
        assert authenticate("bob", "bobpass") != None

    def test_create_user(self):
        # user = create_user("bob", "bobpass")
        user = create_user("rick", "rickpass", "Rick", "White", "9/6/1997", "rick@mail", "BSc. Computer Science")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"user_id":1, "username":"bob"}, {"user_id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class AuthorIntegrationTests(unittest.TestCase):
    def test_create_author(self):
        author = Author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science")
        assert author.firstName == "Bob" and author.lastName == "Moog"

    def test_get_all_authors_json(self):
        author_json=get_all_authors_json()
        self.assertListEqual([{
            'id': 1,
            "firstName": "Bob",
            "lastName": "Moog",
            "dob":datetime.strptime("05/08/2001", "%d/%m/%Y"),
            "email": "bob@mail",
            "qualifications":"BSc. Computer Science"
            },
            {
            'id': 2,
            "firstName": "Rick",
            "lastName": "White",
            "dob":datetime.strptime("9/6/1997", "%d/%m/%Y"),
            "email": "rick@mail",
            "qualifications":"BSc. Computer Science"
            }
            ], author_json)

class PublicationIntegrationTests(unittest.TestCase):
    def test_create_publication(self):
        author = get_author(1)
        authors = []
        if author:
            authors.append(author)
        else:
            authors.append(create_author("Bob","Moog", "05/08/2001","bob@mail", "BSc. Computer Science"))
             
        #coauthors = []
        publication= create_publication("Grandburgh", "Intro to Computer Science", "2018", "10.1080/02626667.2018.1560449", authors)
        assert publication.publisher=="Grandburgh" and publication.title=="Intro to Computer Science" and publication.year=="2018" and publication.doi=="10.1080/02626667.2018.1560449"


    def test_get_publication_json(self):
        publication_json = get_all_publications_json()
        self.assertListEqual([
            {
                "id": 1,
                "publisher": "Grandburgh",
                "title":"Intro to Computer Science",
                "year": "2018",
                "doi": "10.1080/02626667.2018.1560449", 
                "authors":[
                    {
                        "id": 1,
                        "firstName": "Bob",
                        "lastName": "Moog",
                        "dob": datetime.strptime("05/08/2001", "%d/%m/%Y"),
                        "email": "bob@mail",
                        "qualifications": "BSc. Computer Science"
                    }
                ],
    
            }
        ], publication_json)