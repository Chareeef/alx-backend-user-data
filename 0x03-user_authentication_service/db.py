#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""

        # Create user
        user = User()

        # Assign attributes
        user.email = email
        user.hashed_password = hashed_password

        # Save user
        self._session.add(user)
        self._session.commit()

        # Return user
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find and return the first user corresponding to the passed kwargs
        """

        # Check kwargs keys are valid
        valid_keys = ['id', 'email', 'hashed_password',
                      'session_id', 'reset_token']

        for key in kwargs.keys():

            # Raise if wrong key
            if key not in valid_keys:
                raise InvalidRequestError

        # Query for the user
        user = self._session.query(User).filter_by(**kwargs).first()

        # Raise NoResultFound if not found
        if not user:
            raise NoResultFound

        # Return the user
        return user
