#!/usr/bin/env python3
"""The SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from models.user import User


class SessionExpAuth(SessionAuth):
    """Class to manage the Session Authentication for our API
    with Expiration time for sessions
    """

    # Map sessions IDs to their dictionnaries
    user_id_by_session_id = {}

    def __init__(self):
        """Set the duration of Expiration time"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create and return a Session ID for a `user_id`
        """

        # Call parent method to generate a sessions
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Build session dictionnary
        session_dict = {}
        session_dict['user_id'] = user_id
        session_dict['created_at'] = datetime.now()

        # Add it to user_id_by_session_id
        self.user_id_by_session_id[session_id] = session_dict

        # Return the Session Id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """

        # Verify that `session_id` is in user_id_by_session_id
        if session_id not in self.user_id_by_session_id:
            return None

        # Get the session dictionnary
        session_dict = self.user_id_by_session_id[session_id]

        # Return user_id directly if there is no expiration time
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        # Handle expiration time

        # Inacceptable if session_dict doesn't contain 'created_at' key
        if 'created_at' not in session_dict:
            return None

        # Check if already expired
        exp_time = timedelta(seconds=self.session_duration)
        if datetime.now() > session_dict['created_at'] + exp_time:
            return None

        # Return the User ID for this session
        return session_dict.get('user_id')
