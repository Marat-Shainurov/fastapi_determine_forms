from fastapi import FastAPI

from app.forms.routes import forms

app = FastAPI()

app.include_router(forms)
