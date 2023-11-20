from typing import Dict

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator


class FormStructureTemplate(BaseModel):
    name: str = Field(..., min_length=1, title='Form template name.', examples=["Form template name"])
    fields: Dict[str, str] = Field(
        ..., title='Form fields. Available fields types - "email", "text", "phone", "date"',
        examples=[{
            "field_name_1": "field_type",
            "field_name_2": "field_type",
            "field_name_n": "field_type"
        }]
    )

    @model_validator(mode='before')
    @classmethod
    def check_field_types(cls, data):
        for field_name, field_type in data['fields'].items():
            if field_type not in ['email', 'phone', 'date', 'text']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid field type - {field_type}. Supported types: email, phone, date, text."
                )
        return data
