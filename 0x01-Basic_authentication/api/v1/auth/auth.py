#!/usr/bin/env python3
"""The Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return True `path` is not in `excluded_paths`
        with slash tolerance
        Note: All paths in `excluded_paths` end by a '/' or '*'
        """

        # If None or empty
        if not path or not excluded_paths:
            return True

        # Add '/' to `path` if missing
        if not path.endswith('/'):
            path += '/'

        for ex_path in excluded_paths:

            # if ex_path ends with '/'
            if ex_path.endswith('/'):
                if path == ex_path:
                    return False

            # if ex_path endswith '*'
            elif ex_path.endswith('*'):
                if path[:len(ex_path) - 1] == ex_path[:-1]:
                    return False

        # Authorization not required
        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the header request 'Authorization' if it exists
        or None otherwise
        """
        if request:
            return request.headers.get('Authorization', None)
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """To be overloaded"""
        return None
