from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.forms.crud import add_form_template, get_form_templates, get_form_template, update_form_template, \
    delete_form_template_from_db
from app.forms.models import GetFormRequest, FormStructureTemplate

forms = APIRouter()


@forms.post('/get_form/', status_code=status.HTTP_200_OK, tags=["get_form"])
def get_form(fields: GetFormRequest):
    return fields


@forms.post('/create_form_template/',
            response_model=FormStructureTemplate, status_code=status.HTTP_201_CREATED, tags=["form_templates"])
def create_form_template(form_template: FormStructureTemplate):
    form_data = form_template.model_dump()
    new_form_template = add_form_template(form_data)
    return new_form_template


@forms.get('/get_form_templates_list/',
           response_model=list[FormStructureTemplate], status_code=status.HTTP_200_OK, tags=["form_templates"])
def get_form_templates_list():
    return get_form_templates()


@forms.get('/retrieve_form_template/{form_name}',
           response_model=FormStructureTemplate, status_code=status.HTTP_200_OK, tags=["form_templates"])
def retrieve_form_template(form_name: str):
    return get_form_template(form_name)


@forms.put('/put_form_template/{form_name}/',
           response_model=FormStructureTemplate, status_code=status.HTTP_200_OK, tags=["form_templates"])
def put_form_template(form_name: str, form_template: FormStructureTemplate):
    form_data = form_template.model_dump()
    return update_form_template(form_name, form_data)


@forms.delete('/delete_form_template/{form_name}/',
              tags=["form_templates"], status_code=status.HTTP_204_NO_CONTENT)
def delete_form_template(form_name: str):
    delete_form_template_from_db(form_name)
    return JSONResponse(content={"message": f"The form {form_name} has been deleted successfully"})
