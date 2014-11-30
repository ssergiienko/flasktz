from main import db, user_datastore
from models import Role


def create_roles():
    db.session.add(Role('admin'))


def create_user():
    u = user_datastore.create_user(email='m@m.ua', password='password')
    u.roles.append(db.session.query(Role).filter_by(name='admin').one())


def populate_all():
    db.drop_all()
    db.create_all()

    create_roles()
    create_user()

    db.session.commit()

if __name__ == '__main__':
    populate_all()