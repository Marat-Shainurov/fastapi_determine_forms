import re
from typing import Optional, Dict, List

from bson import ObjectId, Regex
from fastapi import status
from fastapi.exceptions import HTTPException
from pymongo.errors import DuplicateKeyError

from app.forms.models import FormStructureTemplate
from config import db


def add_form_template(form_template: Dict) -> Dict:
    """
    Creates a new FormStructureTemplate instance in the database.

    :param form_template: a dictionary of field name / field type pairs ("fields" key), and the form name ("name" key).
    :return: a dictionary type of:
    {'_id': ObjectId('some_id'), 'name': '<form name>', 'fields': {'<field name>': '<fields type>'}},
    :raises HTTPException if the form with provided name already exists in the database.
    """
    try:
        result = db.forms_collection.insert_one(form_template)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The form with provided name already exists'
        )
    created_template = db.forms_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return created_template


def get_form_templates() -> List[FormStructureTemplate]:
    """
    Retrieves a list of stored FormStructureTemplate instances from the database.

    :return: A list of stored FormStructureTemplate instances.
    """
    return db.forms_collection.find()


def update_form_template(form_name: str, form_template: Dict) -> Dict:
    """
    Updates the FormStructureTemplate instance with the form_name name.

    :param form_name: the form name to update (case-insensitive search in the database).
    :param form_template: data to update the form with.
    :return: a dictionary representing the updated instance with new data.
    :raises HTTPException if no form is found with provided name.
    """
    regex_pattern = f'^{re.escape(form_name)}$'
    regex_query = Regex(regex_pattern, 'i')

    form_update = db.forms_collection.find_one_and_update({"name": regex_query}, {"$set": form_template})
    if form_update:
        return db.forms_collection.find_one({'_id': ObjectId(form_update['_id'])})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )


def get_form_template(form_name: str) -> Dict:
    """
    Retrieves the FormStructureTemplate instance with the form_name name from the database.

    :param form_name: the form name to get (case-insensitive search in the database).
    :return: found FormStructureTemplate instance
    :raises HTTPException if no form is found with provided name.
    """
    regex_pattern = f'^{re.escape(form_name)}$'
    regex_query = Regex(regex_pattern, 'i')
    form = db.forms_collection.find_one({'name': regex_query})
    if form:
        return form
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )


def delete_form_template_from_db(form_name: str) -> Optional[Dict]:
    """
    Deletes the FormStructureTemplate instance with the form_name name from the database.

    :param form_name: the form name to get (case-insensitive search in the database).
    :return: Dict of the deleted object | None
    :raises HTTPException if no form is found with provided name.
    """
    regex_pattern = f'^{re.escape(form_name)}$'
    regex_query = Regex(regex_pattern, 'i')
    form_to_delete = db.forms_collection.find_one({'name': regex_query})

    if form_to_delete:
        return db.forms_collection.find_one_and_delete({'name': regex_query})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )
