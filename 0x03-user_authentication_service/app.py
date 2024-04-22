#!/usr/bin/env python3
"""A Flask application
"""
from flask import Flask, jsonify

# Create the app
app = Flask(__name__)

# Disable strict slashes
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Root route
    """
    return jsonify({'message': 'Bienvenue'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
