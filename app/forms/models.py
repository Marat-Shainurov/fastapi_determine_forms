from typing import Dict

from pydantic import BaseModel, Field, model_validator


class FormStructureTemplate(BaseModel):
    name: str = Field(
        ..., min_length=1, title='The Form name. Should be longer than 1 symbol', example='The Form name')
    fields: Dict[str, str] = Field(
        ..., title='The Form fields. Available fields types - "email", "text", "phone", "date"',
        example={
            "field_name_1": "field_type",
            "field_name_2": "field_type",
            "field_name_n": "field_type"
        }
    )

    @model_validator(mode='before')
    @classmethod
    def check_field_types(cls, data):
        for field_name, field_type in data['fields'].items():
            assert (
                    field_type in ['email', 'phone', 'date', 'text']
            ), (f"Invalid field type '{field_type}' for field '{field_name}'."
                f"Supported types: 'email', 'phone', 'date', 'text'.")
        return data


class GetFormRequest(BaseModel):
    field_name: str = Field(...)
    field_value: str = Field(...)
