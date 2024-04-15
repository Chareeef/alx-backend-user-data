#!/usr/bin/env python3
"""The BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class to manage the API Basic Authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if type(authorization_header) is not str or \
                not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header[6:]
