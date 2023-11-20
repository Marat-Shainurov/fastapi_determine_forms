import pytest
from fastapi import status, HTTPException
from fastapi.testclient import TestClient

from app.app_main import app
from app.forms.models import FormStructureTemplate
from config import db

client = TestClient(app)

test_form = dict(
    name='TestForm',
    fields={
        "date_test_field": "date",
        "phone_test_field": "phone",
        "email_test_field": "email",
        "text_test_field": "text"
    })


@pytest.fixture
def cleanup_database():
    yield
    db.forms_collection.delete_one({"name": test_form['name']})


def test_create_form_template(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response = client.post('/create_form_template/', json=new_template.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == new_template.name
    assert response.json()['fields'] == new_template.fields


def test_create_template_invalid_type():
    with pytest.raises(HTTPException) as e:
        invalid_data = dict(name='Form name', fields={'username': 'string'})
        new_template = FormStructureTemplate(**invalid_data)
        client.post('/create_form_template/', json=new_template.model_dump())

    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
    assert e.value.detail == "Invalid field type - string. Supported types: email, phone, date, text."


def test_get_form_successful(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED

    request_data = {
        "date_test_field": "2023-11-20",
        "phone_test_field": "+7 999 888 88 88",
        "email_test_field": "m_shainurov@mail.com",
        "text_test_field": "some value",
        "the_fifth_field": "some text",
        "the_sixth_field": "some content",
        "extra_date_fields": "12-11-2023",
    }
    response_get_form = client.post('/get_form/', json=request_data)
    assert response_get_form.json() == test_form['name']


def test_get_form_invalid_date(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED
    request_data = {
        "date_test_field": "2023,11,20",
        "phone_test_field": "+7 999 888 88 88",
        "email_test_field": "m_shainurov@mail.com",
        "text_test_field": "some value"
    }
    response_get_form = client.post('/get_form/', json=request_data)
    assert response_get_form.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_form.json()['detail'] == 'Invalid "date_test_field" field value. Data type "date"'


def test_get_form_invalid_email(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED
    request_data = {
        "date_test_field": "2023-11-20",
        "phone_test_field": "+7 999 888 88 88",
        "email_test_field": "m_shainurovmail.com",
        "text_test_field": "some value"
    }
    response_get_form = client.post('/get_form/', json=request_data)
    assert response_get_form.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_form.json()['detail'] == 'Invalid "email_test_field" field value. Data type "email"'


def test_get_form_invalid_phone(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED
    request_data = {
        "date_test_field": "2023-11-20",
        "phone_test_field": "+7 9998888888",
        "email_test_field": "m_shainurov@mail.com",
        "text_test_field": "some value"
    }
    response_get_form = client.post('/get_form/', json=request_data)
    assert response_get_form.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_form.json()['detail'] == 'Invalid "phone_test_field" field value. Data type "phone"'


def test_get_form_invalid_phone_no_code(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED
    request_data = {
        "date_test_field": "2023-11-20",
        "phone_test_field": "8 9998888888",
        "email_test_field": "m_shainurov@mail.com",
        "text_test_field": "some value"
    }
    response_get_form = client.post('/get_form/', json=request_data)
    assert response_get_form.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_form.json()['detail'] == 'Invalid "phone_test_field" field value. Data type "phone"'


def test_get_form_no_form_found(cleanup_database):
    new_template = FormStructureTemplate(**test_form)
    response_template = client.post('/create_form_template/', json=new_template.model_dump())
    assert response_template.status_code == status.HTTP_201_CREATED

    request_data_1 = {
        "date_test_field": "2023-11-20",
        "phone_test_field": "+7 999 888 88 88",
    }
    response_get_form = client.post('/get_form/', json=request_data_1)
    assert response_get_form.status_code == status.HTTP_200_OK
    assert response_get_form.json() == {
        'date_test_field': 'date',
        'phone_test_field': 'phone'
    }
