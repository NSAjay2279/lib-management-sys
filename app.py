from flask import Flask, request, jsonify
from typing import Dict, List, Union

app = Flask(__name__)

# In-memory storage
books: List[Dict[str, Union[int, str]]] = []
members: List[Dict[str, Union[int, str]]] = []
AUTH_TOKEN = "secure-token"  # Token for authentication

# Helper function for authentication


def authenticate(token: str) -> bool:
    return token == AUTH_TOKEN


@app.route("/books", methods=["POST"])
def add_book():
    if not authenticate(request.headers.get("Authorization", "")):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    books.append({
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"]
    })
    return jsonify({"message": "Book added successfully"}), 201


@app.route("/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def manage_book(book_id: int):
    if not authenticate(request.headers.get("Authorization", "")):
        return jsonify({"error": "Unauthorized"}), 401
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == "GET":
        return jsonify(book)
    elif request.method == "PUT":
        data = request.json
        book.update(data)
        return jsonify({"message": "Book updated successfully"})
    elif request.method == "DELETE":
        books.remove(book)
        return jsonify({"message": "Book deleted successfully"})


@app.route("/books/search", methods=["GET"])
def search_books():
    query = request.args.get("query", "").lower()
    results = [b for b in books if query in b["title"].lower()
               or query in b["author"].lower()]
    return jsonify(results)


@app.route("/books/paginate", methods=["GET"])
def paginate_books():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    start = (page - 1) * limit
    end = start + limit
    return jsonify(books[start:end])


@app.route("/members", methods=["POST", "GET"])
def manage_members():
    if request.method == "POST":
        data = request.json
        members.append({
            "id": len(members) + 1,
            "name": data["name"],
            "email": data["email"]
        })
        return jsonify({"message": "Member added successfully"}), 201
    elif request.method == "GET":
        return jsonify(members)


if __name__ == "__main__":
    app.run(debug=True)
