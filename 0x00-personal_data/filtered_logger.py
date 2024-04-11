#!/usr/bin/env python3
"""Implement log filters obfuscating some fields
"""
import csv
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in this log record using filter_datum,
        format it and return it
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


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


def get_logger() -> logging.Logger:
    """Return a logging.Logger object"""

    # Create logger
    logger = logging.getLogger('user_data')

    # Set level
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create stream handler
    stream_handler = logging.StreamHandler()

    # Set formatter as RedactingFormatter
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    # Add the handler to logger
    logger.addHandler(stream_handler)

    # Return logger
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a MySQLConnection object based on credentials in os.environ
    """

    # Connect with credentials
    connection = mysql.connector.connect(
            host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.environ.get('PERSONAL_DATA_DB_NAME'),
            user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
            auth_plugin='mysql_native_password'
            )

    # Return connection
    return connection

def main() -> None:
    """Obtain a database connection using get_db,
    retrieve all rows in the users table,
    and display each row under a filtered format
    """

    # Obtain connection
    db = get_db()

    # Retrieve rows
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    # Get logger
    logger = get_logger()

    # Log data
    for row in cursor:
        data = ''
        for i in range(len(row)):
            data += f'{cursor.column_names[i]}={row[i]};'
        logger.info(data)

    # Close resources
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
