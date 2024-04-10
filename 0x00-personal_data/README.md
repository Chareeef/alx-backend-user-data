# Personal Data 

Welcome fellow software engineering enthusiasts! In this guide, we'll dive into the exciting world of managing personal data responsibly and securely. As budding developers, it's crucial for us to understand how to handle Personally Identifiable Information (PII), non-PII, and personal data in our applications. So, let's embark on this enlightening journey together! 

## Understanding Personal Data 

**Personally Identifiable Information (PII)** refers to any data that could potentially identify a specific individual. Examples include: 

- Name
- Address
- Email
- Social Security Number 

**Non-PII** is information that cannot be used on its own to identify, contact, or locate a single person. Examples include: 

- First name without last name
- Country
- Age (without birthdate)
- Gender 

**Personal Data**, as defined by GDPR, is any information related to an identifiable person. It’s a broader category that includes PII and can be something like: 

- IP address
- Location data
- Cookie IDs 

## Implementing PII Obfuscation in Python 

Now, let's get our hands dirty and learn how to implement a log filter in Python that will obfuscate PII fields. By obfuscating sensitive information in our logs, we can prevent unauthorized access to PII and enhance the security of our applications. 

```python
import logging
import re 

def obfuscate_pii(record):
    pii_fields = ['email', 'phone', 'ssn']  # Define PII fields
    for field in pii_fields:
        if field in record.msg:
            record.msg = re.sub(r'\b{}\b'.format(field), '***REDACTED***', record.msg)
    return True 

logger = logging.getLogger(__name__)
logger.addFilter(obfuscate_pii) 

# Now, when we log sensitive information:
logger.warning("User with email john.doe@example.com tried to login.")
# Output: User with email ***REDACTED*** tried to login.
``` 

## Encrypting and Validating Passwords with bcrypt 

Passwords are the keys to our users' kingdoms, so it's crucial to store them securely. One popular approach is to use bcrypt, a powerful hashing algorithm designed for password hashing. Let's see how we can encrypt a password and check the validity of an input password using bcrypt. 

```python
import bcrypt 

def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password 

def validate_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password) 

# Usage example:
password = "supersecret"
hashed_password = encrypt_password(password) 

# Later, when validating a login attempt:
input_password = "supersecret"
if validate_password(input_password, hashed_password):
    print("Login successful!")
else:
    print("Invalid password. Please try again.")
``` 

## Authenticating to a Database Using Environment Variables 

Lastly, let's learn how to authenticate to a database using environment variables. This approach allows us to keep sensitive information like database credentials out of our codebase, minimizing the risk of exposure. 

```python
import os
import mysql.connector 

# Set these in your environment before running the script
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')  # Typically 'localhost' or the server's domain
DB_NAME = os.environ.get('DB_NAME') 

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
) 

# Now, we can execute queries, fetch data, and more!
``` 

## Conclusion 

Congratulations, fellow learners! 🎉 We've covered some essential concepts and techniques for handling personal data securely in our applications. By understanding and implementing these practices, we can build robust and trustworthy software that respects user privacy and security. Keep exploring, keep learning, and let's continue to elevate our skills together! Happy coding! 🚀
