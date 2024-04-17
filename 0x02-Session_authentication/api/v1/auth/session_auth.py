#!/usr/bin/env python3
"""The SessionAuth class"""
from api.v1.auth.auth import Auth
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
