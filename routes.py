from flask import Blueprint, request, jsonify
from typing import Dict, Any, Tuple
import sqlite3

main = Blueprint('main', __name__)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn


@main.route('/books', methods=['POST'])
def create_book() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, description) VALUES (?, ?, ?)',
                   (data['title'], data['author'], data.get('description')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book created successfully'}), 201


@main.route('/books', methods=['GET'])
def get_books() -> Tuple[Dict[str, Any], int]:
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    offset = (page - 1) * limit
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books LIMIT ? OFFSET ?', (limit, offset))
    books = cursor.fetchall()

    total_books = cursor.execute('SELECT COUNT(*) FROM books').fetchone()[0]

    conn.close()

    return jsonify({
        'total': total_books,
        'page': page,
        'limit': limit,
        'books': [dict(book) for book in books]
    }), 200


@main.route('/books/<int:id>', methods=['PUT'])
def update_book(id: int) -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title=?, author=?, description=? WHERE id=?',
                   (data['title'], data['author'], data.get('description'), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated successfully'}), 200


@main.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id: int) -> Tuple[Dict[str, Any], int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully'}), 200


@main.route('/search', methods=['GET'])
def search_books() -> Tuple[Dict[str, Any], int]:
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                   ('%' + query + '%', '%' + query + '%'))
    books = cursor.fetchall()

    conn.close()

    return jsonify([dict(book) for book in books]), 200

# Member CRUD Operations


@main.route('/members', methods=['POST'])
def create_member() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO members (name, email) VALUES (?, ?)',
                       (data['name'], data['email']))
        conn.commit()
        response_message = {'message': 'Member created successfully'}
        status_code = 201
    except sqlite3.IntegrityError:
        response_message = {'message': 'Email already exists'}
        status_code = 400

    conn.close()

    return jsonify(response_message), status_code


@main.route('/members', methods=['GET'])
def get_members() -> Tuple[Dict[str, Any], int]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()

    conn.close()

    return jsonify([dict(member) for member in members]), 200


@main.route('/members/<int:id>', methods=['PUT'])
def update_member(id: int) -> Tuple[Dict[str, Any], int]:
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE members SET name=?, email=? WHERE id=?',
                   (data['name'], data['email'], id))

    if cursor.rowcount == 0:
        return jsonify({'message': 'Member not found'}), 404

    conn.commit()
    conn.close()

    return jsonify({'message': 'Member updated successfully'}), 200


@main.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id: int) -> Tuple[Dict[str, Any], int]:
    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute('DELETE FROM members WHERE id=?', (id,))

    if cursor.rowcount == 0:
        return jsonify({'message': 'Member not found'}), 404

    conn.commit()

    conn.close()

    return jsonify({'message': 'Member deleted successfully'}), 200
