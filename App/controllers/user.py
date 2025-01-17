from App.models import User
from App.database import db

def create_user(username, password, firstName, lastName, dob, email, qualifications):
    newuser = User(username=username, password=password, firstName=firstName, lastName=lastName, dob=dob, email=email, qualifications=qualifications)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(user_id, username):
    user = get_user(user_id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    