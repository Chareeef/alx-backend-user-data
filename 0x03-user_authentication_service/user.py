#!/usr/bin/env python3
"""The User model"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

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
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String)
    reset_token = Column(String)
