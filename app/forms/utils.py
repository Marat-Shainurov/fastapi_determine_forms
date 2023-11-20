from datetime import datetime
from typing import List, Dict

from fastapi import HTTPException, status

from app.forms.validators import is_phone_number_valid, DATA_TYPE_VALIDATORS
from config import db


def determine_data_type(field_value: str) -> str:
    """
    Validates and assigns the data type for the passed field_value.
    Allowed data types: date, phone, email, text. Validates data type-wise in the same order.

    :param field_value: a string representing a field's value to validate and determine the data type for.
    :return: a string representing the field_value data type after the validation process.
    """
    try:
        datetime_obj = datetime.strptime(field_value, '%d.%m.%Y')
        return 'date'
    except ValueError:
        pass
    try:
        datetime_obj = datetime.strptime(field_value, '%Y-%m-%d')
        return 'date'
    except ValueError:
        pass

    if is_phone_number_valid(field_value):
        return 'phone'
    else:
        if '@' in field_value and '.' in field_value:
            return 'email'
        else:
            return 'text'


def search_for_form(form_request: Dict[str, str]):
    """
    Searches the most suitable form template in the database.
    Returns the found template name if:
    - all the fields names of the found template provided in form_request.
    - all the fields values in form_request pass the data type validation process.

    Narrows down the primary database query result via the "$or" and "$exists" operators, to process only the templates
    that contain at least one field provided in form_request.

    :param form_request: a form request body, type of Dict[str, str]
    :return: the found form's name,
    or a dictionary type of Dict[str, str] with field names and filed data types if the search requirements aren't met.
    """

    form_request_fields = set(form_request.keys())
    templates_with_request_fields = db.forms_collection.find(
        {
            "$or": [
                {f'fields.{field}': {'$exists': True}} for field in form_request_fields
            ]
        })
    if templates_with_request_fields:
        for template in templates_with_request_fields:
            template_fields_names = set(template['fields'].keys())
            if form_request_fields.issuperset(template_fields_names):
                similar_fields = form_request_fields & template_fields_names
                for field in similar_fields:
                    data_to_validate = form_request[field]
                    data_type = template['fields'][field]
                    if data_type != 'text' and not DATA_TYPE_VALIDATORS[data_type](data_to_validate):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid "{field}" field value. Data type "{data_type}"')
                return template['name']
        else:
            return {field: determine_data_type(field_value) for field, field_value in form_request.items()}
