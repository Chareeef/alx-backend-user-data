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


def _hash_password(password: str) -> bytes:
    """Hash `password` and returns a salted, hashed password,
    which is a byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """The function should return a string representation of a new UUID
    """
    return str(uuid.uuid4())
