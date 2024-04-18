#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class to keep track of sessions IDs in a database
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance with session ID and its user ID
        """
        super().__init__(*args, **kwargs)
        self.session_id = kwargs.get('session_id')
        self.user_id = kwargs.get('user_id')
