from functools import wraps
from flask import request, jsonify

TOKEN = "your_secure_token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != TOKEN:
            return jsonify({'message': 'Token is missing or invalid!'}), 403
        return f(*args, **kwargs)

    return decorated

@main.route('/members', methods=['POST'])
@token_required
def create_member():
    data = request.get_json()
    # Similar logic to create a member in database...
