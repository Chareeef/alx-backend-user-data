#!/usr/bin/env python3
"""The BasicAuth class"""
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Class to manage the API Basic Authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if not isinstance(authorization_header, str) or \
                not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """Return the decoded value of a
        Base64 string `base64_header`
        """
        if not isinstance(base64_header, str):
            return None

        try:
            header_bytes = base64_header.encode('utf-8')
            return base64.decodebytes(header_bytes).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_header: str) -> (str, str):
        """Return the user email and password from the Base64 decoded value"""
        if not isinstance(decoded_base64_header, str) or \
                ':' not in decoded_base64_header:
            return (None, None)
        else:
            return tuple(decoded_base64_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if not isinstance(user_email, str) or \
                not isinstance(user_pwd, str):
            return None

        # Search for email
        try:
            user = User.search({'email': user_email})[0]
        except IndexError:
            return None

        # Check password
        if user.is_valid_password(user_pwd):
            return user
        else:
            return None
