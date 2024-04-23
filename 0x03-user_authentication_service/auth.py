#!/usr/bin/env python3
"""Passwords Encryption/Decryption"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database
        """

        # If the email already exists
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        # Create the user
        user = self._db.add_user(email, _hash_password(password))

        # Return it
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check that the credentials are correct
        """

        # Verify that email is registered
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # Verify that password is correct
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """Create a session ID for the user with email and return this ID
        """

        # Find the user
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        # Create and assign session ID
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        # Return the session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Takes a single `session_id` string argument
        and returns the corresponding User or None
        """

        # Search and return the user if exists, otherwise return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the user's session
        """

        try:

            # Update the user’s session ID to None
            self._db.update_user(user_id, session_id=None)

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token for the user
        """

        # Find the user
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        # Generate token
        reset_token = _generate_uuid()

        # Assign it
        self._db.update_user(user.id, reset_token=reset_token)

        # Return it
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the user's password, requiring reset_token
        """

        # Find the user
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        # Update user's password
        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password, 
                             reset_token=None)


def _hash_password(password: str) -> bytes:
    """Hash `password` and returns a salted, hashed password,
    which is a byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """The function should return a string representation of a new UUID
    """
    return str(uuid.uuid4())
