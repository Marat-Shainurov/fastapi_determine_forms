import re
from datetime import datetime

from email_validator import validate_email, EmailNotValidError


def is_phone_number_valid(phone_number):
    """
    Checks whether phone_number aligns with the pattern +7 xxx xxx xx xx.

    :param phone_number: a string representing the phone number to validate.
    :return: True if the validation process is passed, otherwise returns False.
    """
    pattern = re.compile(r'\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}')
    if pattern.fullmatch(phone_number):
        return True
    else:
        return False


def is_date_format_valid(date_string):
    """
    Checks whether date_string aligns with the patterns DD.MM.YYYY or YYYY-MM-DD.

    :param date_string: a string representing the date to validate.
    :return: True if the validation process is passed, otherwise returns False.
    """
    try:
        datetime_obj = datetime.strptime(date_string, '%d.%m.%Y')
        return True
    except ValueError:
        pass
    try:
        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        pass

    return False


def is_email_valid(email_string):
    """
    Validates email_string via email_validator.validate_email.

    :param email_string: a string representing the email address to validate.
    :return: True if the validation process is passed, otherwise returns False.
    """
    try:
        email_info = validate_email(email_string, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


DATA_TYPE_VALIDATORS = {
    'date': is_date_format_valid,
    'phone': is_phone_number_valid,
    'email': is_email_valid,
}
