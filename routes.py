from flask import Blueprint, request, jsonify
import sqlite3

main = Blueprint('main', __name__)


def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn


@main.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, description) VALUES (?, ?, ?)',
                   (data['title'], data['author'], data.get('description')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book created successfully'}), 201


@main.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return jsonify([dict(book) for book in books]), 200


@main.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title=?, author=?, description=? WHERE id=?',
                   (data['title'], data['author'], data.get('description'), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated successfully'}), 200


@main.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully'}), 200


@main.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()
    conn.close()
    return jsonify([dict(book) for book in books]), 200
