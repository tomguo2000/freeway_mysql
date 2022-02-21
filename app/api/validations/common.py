import re

name_regex = r"(^[a-zA-Z\s\-]+$)"
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_regex = r"(^[a-zA-Z0-9_]+$)"

dangerous_chars = "~;!@#$%^&*()_+-*<>,[]"

def is_name_valid(name):
    """Checks if name input is within the acceptable pattern defined in name_regex.

    Args:
        name: string input for name.

    Return:
        True: if string input for name is within the acceptable name_regex pattern.
        False: if string input for name is not according to name_regex pattern.
    """
    return re.match(name_regex, name)


def is_email_valid(email):
    """Checks if email input is within the acceptable pattern defined in email_regex.

    Args:
        email: string input for email.

    Return:
        True: if string input for email is within the acceptable email_regex pattern.
        False: if string input for email is not according to email_regex pattern.
    """
    return re.match(email_regex, email)


def is_username_valid(username):
    """Checks if username input is within the acceptable pattern defined in username_regex.

    Args:
        name: string input for username.

    Return:
        True: if string input for username is within the acceptable username_regex pattern.
        False: if string input for username is not according to username_regex pattern.
    """
    return re.match(username_regex, username)


def include_dangerous_chars(data):
    data = str(data)
    for i in dangerous_chars:
        if i in data:
            print(f'NOOOOO, find this : {i} in data!')
            return True

    return False