#!/usr/bin/env python3
"""The SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """Class to manage the Session Authentication for our API
    with Expiration time and File storage for sessions IDs
    """

    def create_session(self, user_id: str = None) -> str:
        """Create and return a Session ID for a `user_id`
        """

        # Verify `user_id`'s type
        if not isinstance(user_id, str):
            return None

        # Generate a Session ID
        session_id = str(uuid.uuid4())

        # Store new instance of UserSession
        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()

        # Return the Session Id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID by querying UserSession DB
        """

        # Get the UserSession if it exists within UserSession DB
        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except BaseException:
            return None

        # Return user_id directly if there is no expiration time
        if self.session_duration <= 0:
            return user_session.user_id

        # Handle expiration time

        # Inacceptable if user_session doesn't contain 'created_at' key
        if not isinstance(user_session.created_at, datetime):
            return None

        # Check if already expired
        exp_time = timedelta(seconds=self.session_duration)
        if datetime.utcnow() > user_session.created_at + exp_time:
            return None

        # Return the User ID for this session
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session, e.g.: logout"""

        if not request:
            return False

        # Retrieve session ID
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Verify it is linked to a user
        if not self.user_id_for_session_id(session_id):
            return False

        # Delete it from UserSession DB and return True
        user_session = UserSession.search({'session_id': session_id})[0]
        user_session.remove()

        return True
