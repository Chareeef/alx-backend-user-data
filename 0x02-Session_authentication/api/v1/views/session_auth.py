#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/session_auth/login/
    Login through Session Authentication

    Return the JSON representation of the logged user
    """

    # Retrieve email
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'email missing'}), 400

    # Retrieve password
    password = request.form.get('password')
    if not password:
        return jsonify({'error': 'password missing'}), 400

    # Search the user
    try:
        user = User.search({'email': email})[0]
    except BaseException:
        return jsonify({'error': 'no user found for this email'}), 404

    # Verify password
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    # Create a session for this user
    else:
        from api.v1.app import auth

        # Create session ID for this user
        session_id = auth.create_session(user.id)

        # Build and return the response with the user's JSON
        # and the session cookie set
        response = make_response(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)

        return response
