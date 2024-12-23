from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id:int
    nombre:str
    apellido:str
    direccion:Optional[str]
    telefono:int
    creacion_user:datetime = datetime.now()

class LoginData(User):
    username: str
    password: str

class PyUser(User):
    id: int
    permissions: list[str] = []

class Token(BaseModel):
    access_token: str
    token_type: str
