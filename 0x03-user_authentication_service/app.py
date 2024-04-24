#!/usr/bin/env python3
"""A Flask application
"""
from auth import Auth
from flask import (abort, Flask, jsonify, make_response,
                   redirect, request, url_for)

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
    return make_response(jsonify({'message': 'Bienvenue'}))


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
    return make_response(jsonify({'email': email, 'message': 'user created'}))


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


@app.route('/sessions/', methods=['DELETE'])
def logout() -> str:
    """Destroy the session for the user
    """

    # Retrieve the session ID from the cookie
    session_id = request.cookies.get('session_id')

    # Send 'Forbidden' if no session ID was sent
    if not session_id:
        abort(403)

    # Search for the user
    user = AUTH.get_user_from_session_id(session_id)

    # Send 'Forbidden' if not found
    if not user:
        abort(403)

    # Destroy session
    AUTH.destroy_session(user.id)

    # Redirect to root
    return redirect(url_for('index'))


@app.route('/profile/')
def profile():
    """Return the user's email based on `session_id`
    """

    # Retrieve the session ID from the cookie
    session_id = request.cookies.get('session_id')

    # Send 'Forbidden' if no session ID was sent
    if not session_id:
        abort(403)

    # Search for the user
    user = AUTH.get_user_from_session_id(session_id)

    # Send 'Forbidden' if no user was found
    if not user:
        abort(403)

    # Return email payload
    return make_response(jsonify({'email': user.email}))


@app.route('/reset_password/', methods=['POST'])
def get_reset_password_token():
    """Generate reset password token for a user
    """

    # Retrieve email
    email = request.form.get('email')

    try:
        # Generate the reset password token for the user if exists
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    # Return email and reset_token payload
    return make_response(jsonify({'email': email,
                                  'reset_token': reset_token}))


@app.route('/reset_password/', methods=['PUT'])
def update_password():
    """Update the user's password, requiring reset_token
    """

    # Retrieve email, new password and reset_token
    email = request.form.get('email')
    password = request.form.get('password')
    reset_token = request.form.get('reset_token')

    # Send 'Forbidden' if no reset_token was sent
    if not reset_token:
        abort(403)

    try:
        # Update the user's password
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)

    # Return message payload
    return make_response(jsonify({'email': email,
                                  'message': 'Password updated'}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
