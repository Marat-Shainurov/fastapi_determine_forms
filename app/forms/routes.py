from typing import List, Dict

from fastapi import APIRouter, status, Body, Query
from fastapi.responses import JSONResponse

from app.forms.crud import add_form_template, get_form_templates, get_form_template, update_form_template, \
    delete_form_template_from_db
from app.forms.models import FormStructureTemplate
from app.forms.utils import search_for_form

forms = APIRouter()


@forms.post(
    '/get_form', status_code=status.HTTP_200_OK, tags=["get_form"])
def get_form(form_request: Dict[str, str] = Body(..., examples=[
    {
        "field_name_1": "field_value",
        "field_name_2": "field_value",
        "field_name_n": "field_value"
    }
])):
    """
    Endpoint searches the form template which has **all the fields names provided in form_request**.
    If the form is found and **all fields values in form_request pass the data type validation process**,
    it returns the found form's name.

    - **_form_request_**: request form to match stored form templates with.
    """
    search_result = search_for_form(form_request)
    return search_result


@forms.post('/create_form_template',
            response_model=FormStructureTemplate, status_code=status.HTTP_201_CREATED, tags=["form_templates"])
def create_form_template(form_template: FormStructureTemplate):
    """
    Endpoint for creating a new form template instance in the database.
    Allowed fields types: **date, phone, email, text**.

    - **_form_template_**: a new form template schema, based on the FormStructureTemplate pydantic model.

    Returns the created form template.
    """
    form_data = form_template.model_dump()
    new_form_template = add_form_template(form_data)
    return new_form_template


@forms.get('/get_form_templates_list',
           response_model=list[FormStructureTemplate], status_code=status.HTTP_200_OK, tags=["form_templates"])
def get_form_templates_list():
    """
    Endpoint for retrieving a list of form template instances stored in the database.
    Returns the list of found form templates.
    """
    return get_form_templates()


@forms.get('/retrieve_form_template/{form_name}',
           response_model=FormStructureTemplate, status_code=status.HTTP_200_OK, tags=["form_templates"])
def retrieve_form_template(form_name: str):
    """
    Endpoint for retrieving a form template instance stored in the database with form_name.

    - **_form_name_**: a form template name to retrieve (case-insensitive search in the database).

    Returns the found form template.
    """
    return get_form_template(form_name)


@forms.put('/put_form_template/{form_name}',
           response_model=FormStructureTemplate, status_code=status.HTTP_200_OK, tags=["form_templates"])
def put_form_template(form_name: str, form_template: FormStructureTemplate):
    """
    Endpoint for updating a form template instance stored in the database with form_name.

    - **_form_name_**: a form template name to update (case-insensitive search in the database).
    - **_form_template_**: data to update the form template with.

    Returns the updated form template.
    """
    form_data = form_template.model_dump()
    return update_form_template(form_name, form_data)


@forms.delete('/delete_form_template/{form_name}',
              tags=["form_templates"], status_code=status.HTTP_204_NO_CONTENT)
def delete_form_template(form_name: str):
    """
    Endpoint for deleting a form template instance stored in the database with form_name.

    - **_form_name_**: a form template name to delete from the database (case-insensitive search in the database).
    """
    delete_form_template_from_db(form_name)
    return JSONResponse(content={"message": f"The form {form_name} has been deleted successfully"})
