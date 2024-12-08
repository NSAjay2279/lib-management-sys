@main.route('/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    conn.close()
    return jsonify([dict(member) for member in members]), 200

@main.route('/members/<int:id>', methods=['PUT'])
@token_required
def update_member(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE members SET name=?, email=? WHERE id=?',
                   (data['name'], data['email'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Member updated successfully'}), 200


@main.route('/members/<int:id>', methods=['DELETE'])
@token_required
def delete_member(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM members WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Member deleted successfully'}), 200


@main.route('/books', methods=['GET'])
def get_books():
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
