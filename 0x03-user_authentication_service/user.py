#!/usr/bin/env python3
"""User module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create our Base class
Base = declarative_base()


class User(Base):
    """The User model mapped to the `users` table

    Attributes:
        id: the integer primary key
        email: a non-nullable string
        hashed_password: a non-nullable string
        session_id: a nullable string
        reset_token: a nullable string
    """

    # Table name
    __tablename__ = 'users'

    # Columns
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        """Representation of the user instance
        """
        return f'User ({self.id}): {self.email} - {self.hashed_password}'
