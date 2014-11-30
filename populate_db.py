# coding: utf-8

from main import db, user_datastore
from models import Role, Author, Book


def create_roles():
    db.session.add(Role('admin'))


def create_user():
    u = user_datastore.create_user(email='m@m.ua', password='password')
    u.roles.append(db.session.query(Role).filter_by(name='admin').one())


def create_books():
    b = Book(u'Война и мир')
    a = Author(u'Толстой')
    b.authors.append(a)
    db.session.add(b)

    b = Book(u'Финансист')
    a = Author(u'Теодор Драйзер')
    b.authors.append(a)
    db.session.add(b)

    b = Book(u'Dive into Python')
    a = Author(u'Марк Пилгрим')
    b.authors.append(a)
    db.session.add(b)


def populate_all():
    db.drop_all()
    db.create_all()

    create_roles()
    create_user()
    create_books()

    db.session.commit()

if __name__ == '__main__':
    populate_all()