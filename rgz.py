from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# Создание Blueprint
rdz_bp = Blueprint('rdz', __name__, template_folder='templates', static_folder='static')

# Инициализация базы данных
db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    cover_url = db.Column(db.String(250), nullable=True)

@rdz_bp.route('/')
def index():
    return render_template('index.html')

@rdz_bp.route('/books', methods=['GET', 'POST'])
def books():
    page = request.args.get('page', 1, type=int)
    query = Book.query
    
    # Фильтрация
    if 'title' in request.args:
        query = query.filter(Book.title.ilike(f"%{request.args['title']}%"))
    if 'author' in request.args:
        query = query.filter(Book.author.ilike(f"%{request.args['author']}%"))
    if 'min_pages' in request.args:
        query = query.filter(Book.pages >= int(request.args['min_pages']))
    if 'max_pages' in request.args:
        query = query.filter(Book.pages <= int(request.args['max_pages']))
    if 'publisher' in request.args:
        query = query.filter(Book.publisher.ilike(f"%{request.args['publisher']}%"))

    # Сортировка
    if 'sort' in request.args:
        sort_field = request.args['sort']
        query = query.order_by(sort_field)
    
    books = query.paginate(page, 20, False)
    return render_template('books.html', books=books)

@rdz_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Добавление новой книги
        title = request.form['title']
        author = request.form['author']
        pages = int(request.form['pages'])
        publisher = request.form['publisher']
        cover_url = request.form['cover_url']
        
        new_book = Book(title=title, author=author, pages=pages, publisher=publisher, cover_url=cover_url)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('rdz.admin'))

    books = Book.query.all()
    return render_template('admin.html', books=books)
