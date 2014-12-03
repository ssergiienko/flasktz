# coding: utf-8

from wtforms.ext.sqlalchemy.orm import model_form
from models import db, Book, Author

BookForm = model_form(Book, db_session=db.session)
AuthorForm = model_form(Author, db_session=db.session)