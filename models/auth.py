from fastapi.params import Form
from pydantic import BaseModel


class Auth(BaseModel):
    id: str = Form(...)
    password: str = Form(...)
