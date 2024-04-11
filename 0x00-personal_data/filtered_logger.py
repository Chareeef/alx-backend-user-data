#!/usr/bin/env python3
"""Implement log filters obfuscating some fields
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate the log message, and return the obfuscated message.

    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in the log line (message)
    """
    obf_msg = message
    for f in fields:
        obf_msg = re.sub(r'{}=.*?{}'.format(f, separator),
                         f'{f}={redaction}{separator}', obf_msg)
    return obf_msg
