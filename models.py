# coding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import RoleMixin, UserMixin

db = SQLAlchemy()


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return u"Role(name='{0}')".format(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return u"User(email='{0}')".format(self.email)


books_authors = db.Table('books_authors',
    db.Column('book_id', db.Integer(), db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer(), db.ForeignKey('author.id')))


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return u"Book(title='{0}')".format(self.title).encode('utf-8')


class Author(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    books = db.relationship('Book', secondary=books_authors, backref=db.backref('authors', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return u"Author(name='{0}')".format(self.name).encode('utf-8')