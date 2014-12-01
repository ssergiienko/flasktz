# coding: utf-8

from flask import Flask, render_template, request, jsonify
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, roles_required, current_user

from models import db, User, Role, Book, Author

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'jg2jklrqwioptopk5900-349238eiopfeopw0-12'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def init_data():
    from populate_db import populate_all
    populate_all()


@app.route('/')
def index():
    return render_template('layout_page.html')


@app.route('/books/')
def all_books():
    books = db.session.query(Book).all()
    return render_template('books_page.html', data=books)


@app.route('/authors/')
def all_authors():
    authors = db.session.query(Author).all()
    return render_template('authors_page.html', data=authors)


@app.route('/search/')
def search_books():
    s_string = request.args.get('str', '')
    if s_string:
        books = Book.query.filter(Book.title.contains(s_string)).all()
    else:
        books = []
    # Такое усложнение из-за https://github.com/mitsuhiko/flask/issues/673
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    return jsonify({n: book.title for n, book in enumerate(books)})

@app.route('/authorized/')
@login_required
@roles_required('admin')
def secret():
    return 'something secret...'

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)