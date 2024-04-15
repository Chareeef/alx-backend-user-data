#!/usr/bin/env python3
"""The BasicAuth class"""
from api.v1.auth.auth import Auth
import base64
import binascii


class BasicAuth(Auth):
    """Class to manage the API Basic Authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if not isinstance(authorization_header, str) or \
                not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """Returns the decoded value of a
        Base64 string `base64_header`
        """
        if not isinstance(base64_header, str):
            return None

        try:
            header_bytes = base64_header.encode('utf-8')
            return base64.decodebytes(header_bytes).decode('utf-8')
        except binascii.Error:
            return None
