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
        """Return the decoded value of a Base64 string `base64_header`
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
            # Handle passwords containing ':'

            # Index of the separating ':'
            first_colon_idx = decoded_base64_header.find(':')

            # Get email and password slices
            email = decoded_base64_header[:first_colon_idx]
            password = decoded_base64_header[first_colon_idx + 1:]

            # Return credentials
            return (email, password)

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
        except BaseException:
            return None

        # Check password
        if user.is_valid_password(user_pwd):
            return user
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request"""

        # Retrieve the 'Authorization' header value
        auth_value = self.authorization_header(request)
        if not auth_value:
            return None

        # Get the Base 64 part if provided
        base64_part = self.extract_base64_authorization_header(auth_value)
        if not base64_part:
            return None

        # Decode the Base 64 part
        decoded_str = self.decode_base64_authorization_header(base64_part)
        if not decoded_str:
            return None

        # Try to extract email and password
        credentials = self.extract_user_credentials(decoded_str)
        if not credentials:
            return None

        # Find and Return the user if `credentials` are correct,
        # Return None otherwise
        return self.user_object_from_credentials(*credentials)
