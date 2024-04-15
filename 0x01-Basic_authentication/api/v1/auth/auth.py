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
        Note: All paths in `excluded_paths` end by a '/'
        """

        # If None or empty
        if not path or not excluded_paths:
            return True

        # Add a '/' to the end of `path` if it doesn't have it
        if not path.endswith('/'):
            path += '/'

        # Return the membership test result
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
