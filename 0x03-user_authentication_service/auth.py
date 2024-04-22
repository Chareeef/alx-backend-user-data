#!/usr/bin/env python3
"""Passwords Encryption/Decryption"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash `password` and returns a salted, hashed password,
    which is a byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
