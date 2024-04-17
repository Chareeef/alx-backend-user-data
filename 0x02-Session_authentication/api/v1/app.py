#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# auth variable
auth = None

auth_type = getenv('AUTH_TYPE')

if auth_type == 'auth':
    # Assign an Auth instance
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    # Assign a BasicAuth instance
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'session_auth':
    # Assign a SessionAuth instance
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request():
    """Runs before every request"""
    global auth

    if not auth:
        return

    elif not auth.require_auth(request.path,
                               ['/api/v1/status/',
                                '/api/v1/unauthorized/',
                                '/api/v1/forbidden/']):
        return

    elif not auth.authorization_header(request):
        abort(401)

    elif not auth.current_user(request):
        abort(403)

    else:
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
