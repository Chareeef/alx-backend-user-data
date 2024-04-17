#!/usr/bin/env python3
"""The SessionAuth class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Class to manage the Session Authentication for our API
    """

    # Map users IDs to sessions IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create and return a Session ID for a `user_id`
        """

        # Verify `user_id`'s type
        if not isinstance(user_id, str):
            return None

        # Generate a Session ID
        session_id = str(uuid.uuid4())

        # Map this Session ID to `user_id`
        self.user_id_by_session_id[session_id] = user_id

        # Return the Session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """

        # Verify `session_id`'s type
        if not isinstance(session_id, str):
            return None

        # Try to get `user_id` if exists, None otherwise
        user_id = self.user_id_by_session_id.get(session_id)

        # Return the User ID
        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request"""

        if not request:
            return None

        # Get the Session ID based on the request's session cookie
        session_id = self.session_cookie(request)

        # Get the User ID based on the Session ID
        user_id = self.user_id_for_session_id(session_id)

        # Return the user if exists
        return User.get(user_id)
