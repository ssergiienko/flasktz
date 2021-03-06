# coding: utf-8

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, roles_required

from models import db, User, Role, Book, Author
from forms import BookForm, AuthorForm

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
    books = Book.query.all()
    return render_template('books_all_page.html', books=books)


@app.route('/authors/')
def all_authors():
    authors = Author.query.all()
    return render_template('authors_all_page.html', authors=authors)


@app.route('/search/<s_string>')
def search_books(s_string):
    if s_string:
        books = Book.query.filter(Book.title.contains(s_string)).all()
        if not books:   # fallback to search by author
            books = Book.query.filter(Book.authors.any(Author.name.contains(s_string))).all()
    else:
        books = []
    # Такое усложнение из-за https://github.com/mitsuhiko/flask/issues/673
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    return jsonify({n: book.title for n, book in enumerate(books)})


@app.route('/authors/create/', methods=('GET', 'POST',))
@login_required
@roles_required('admin')
def create_author():
    if request.method == 'GET':
        form = AuthorForm()
    else:   # POST
        form = AuthorForm(request.form)
        if form.validate():
            author = Author('')
            form.populate_obj(author)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('edit_authors'))
    return render_template('authors_edit_page.html', form=form)


@app.route('/authors/edit/<int:id_>', methods=('GET', 'POST', 'DELETE'))
@app.route('/authors/edit/')
@login_required
@roles_required('admin')
def edit_authors(id_=None):
    if id_ is None:
        authors = Author.query.all()
        return render_template('authors_list_page.html', authors=authors)
    else:
        author = Author.query.get_or_404(id_)
        if request.method == 'GET':
            form = AuthorForm(obj=author)
        elif request.method == 'POST':
            form = AuthorForm(request.form)
            if form.validate():
                form.populate_obj(author)
                db.session.add(author)
                db.session.commit()
                return redirect(url_for('edit_authors'))
        else:    # request.method == 'DELETE'
            db.session.delete(author)
            db.session.commit()
            return '', 200
    return render_template('authors_edit_page.html', form=form, obj_id=author.id)


@app.route('/books/create/', methods=('GET', 'POST',))
@login_required
@roles_required('admin')
def create_book():
    if request.method == 'GET':
        form = BookForm()
    else:   # POST
        form = BookForm(request.form)
        if form.validate():
            book = Book('')
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('edit_books'))
    return render_template('books_edit_page.html', form=form)


@app.route('/books/edit/<int:id_>', methods=('GET', 'POST', 'DELETE'))
@app.route('/books/edit/')
@login_required
@roles_required('admin')
def edit_books(id_=None):
    if id_ is None:
        books = Book.query.all()
        return render_template('books_list_page.html', books=books)
    else:
        book = Book.query.get_or_404(id_)
        if request.method == 'GET':
            form = BookForm(obj=book)
        elif request.method == 'POST':
            form = BookForm(request.form)
            if form.validate():
                form.populate_obj(book)
                db.session.add(book)
                db.session.commit()
                return redirect(url_for('edit_books'))
        else:    # request.method == 'DELETE'
            db.session.delete(book)
            db.session.commit()
            return '', 200
    return render_template('books_edit_page.html', form=form, obj_id=book.id)

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)