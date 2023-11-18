from bson import ObjectId
from fastapi import status
from fastapi.exceptions import HTTPException
from pymongo.errors import DuplicateKeyError

from config import db


def add_form_template(form_template: dict) -> dict:
    try:
        result = db.forms_collection.insert_one(form_template)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The form with provided name already exists'
        )
    created_template = db.forms_collection.find_one({"_id": ObjectId(result.inserted_id)})
    return created_template


def get_form_templates():
    return db.forms_collection.find()


def update_form_template(form_name: str, form_template: dict):
    form_update = db.forms_collection.find_one_and_update({"name": form_name}, {"$set": form_template})
    if form_update:
        return db.forms_collection.find_one({'_id': ObjectId(form_update['_id'])})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )


def get_form_template(form_name: str):
    form = db.forms_collection.find_one({'name': form_name})
    if form:
        return form
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )


def delete_form_template_from_db(form_name):
    form_to_delete = db.forms_collection.find_one({'name': form_name})
    if form_to_delete:
        return db.forms_collection.find_one_and_delete({'name': form_name})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No form template with {form_name} name found.'
        )
