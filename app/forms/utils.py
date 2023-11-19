from datetime import datetime

from fastapi import HTTPException, status

from app.forms.validators import is_phone_number_valid, DATA_TYPE_VALIDATORS
from config import db


def determine_data_type(field_value):
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


def search_for_form(form_request: list):
    form_request_fields = set([field['field_name'] for field in form_request])
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
                    data_to_validate = [f['field_value'] for f in form_request if f['field_name'] == field][0]
                    data_type = template['fields'][field]
                    if data_type != 'text' and not DATA_TYPE_VALIDATORS[data_type](data_to_validate):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid "{field}" field value. Data type "{data_type}"')
                return template['name']
        else:
            return {field['field_name']: determine_data_type(field['field_value']) for field in form_request}
