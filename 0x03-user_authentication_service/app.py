#!/usr/bin/env python3
"""A Flask application
"""
from auth import Auth
from flask import abort, Flask, jsonify, make_response, request

# Create the app
app = Flask(__name__)

# Disable strict slashes
app.url_map.strict_slashes = False

# Instantiate Auth
AUTH = Auth()


@app.route('/')
def index():
    """Root route
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users/', methods=['POST'])
def users():
    """End-point to register a user
    """

    # Retrieve email and password
    email = request.form.get('email')
    password = request.form.get('password')

    # Try to register the user
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400

    # The user was successefully registered
    return jsonify({'email': email, 'message': 'user created'})


@app.route('/sessions/', methods=['POST'])
def login():
    """Create a new login session for the user
    """

    # Retrieve email and password
    email = request.form.get('email')
    password = request.form.get('password')

    # Check credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session
    session_id = AUTH.create_session(email)

    # Make and send response
    response = make_response(jsonify({'email': email, 'message': 'logged in'}))
    response.set_cookie('session_id', session_id)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)