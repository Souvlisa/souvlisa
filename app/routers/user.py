from fastapi import APIRouter, Depends, HTTPException, Request, security, status
from app.schemas import User
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.testclient import TestClient
from pydantic import BaseModel
from jose import jwt 
from typing import Annotated, Any
import bcrypt
from app.schemas import PyUser, LoginData, Token
from datetime import datetime


router = APIRouter(
    prefix = "/user",
    tags = ['Users'] 
)

Usuarios = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={'items': 'permissions to access items'})
users = {
    "lisa": {"username": "lisa","role": "admin", "email": "luisangelilozada@gmailcom", "password": "lisa25", 'permissions': ['items:read', 'items:write', 'users:read', 'users:write']},
    "user2": {"username": "user2","role": "user", "email": "user2@gmailcom", "password": "user2",'permissions': ['items:read']}
}

def authenticate_user(username: str, password: str) -> PyUser:
    exception = HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid credentials'
                )
    for obj in users:
        if obj['username'] == username:
            if not bcrypt.checkpw(password.encode(), obj['password'].encode()):
                raise exception
            user = PyUser(**obj)
            return user

def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> PyUser:
    decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = decoded['sub']
    for obj in users:
        if obj['username'] == username:
            user = PyUser(**obj)
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials'
    )
def create_token(user: PyUser) -> str:
    payload = {'sub': user.username, 'iat': datetime.datetime.utcnow(),
               'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)}
    token = jwt.encode(payload, key='secret')
    return token


def encode_token (payload: dict)-> str:
    token = jwt .encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)])-> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    token = encode_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")

def get_user(current_user: PyUser = Depends(get_current_user)):
    return current_user

@router.get ('/')
def obtener_usuarios():
    return Usuarios

@router.post('/')

def crear_usuario(usuario:User):
    user = usuario.model_dump()
    Usuarios.append(user)
    print(user)
    return{'Usuario creado exitosamente'}

@router.get('/{user_id}')

def obtener_usuario(user_id:int):
    for user in Usuarios:
        print(user, type(user))
        if user['id'] == user_id:
            return {'Usuario': user}
        return {'repuesta': 'Usuario no encontrado'}

@router.delete('/{user_id}')

def eliminar_usuario(user_id:int):
    for index, user in enumerate(Usuarios):
        if user['id'] == user_id:
            Usuarios.pop(index)
            return {'respuesta': 'Usuario eliminado correctamente'} 
        return {'respuesta': 'Usuario no encontrado'}

@router.put('/{user_id}')

def actualizar_usuario(user_id:int, updateUser: User):
        for index, user in enumerate(Usuarios):
            if user['id'] == user_id:
                Usuarios[index]['id'] = updateUser.model_dump()['id']
                Usuarios[index]['nombre'] = updateUser.model_dump()['nombre']
                Usuarios[index]['apellido'] = updateUser.model_dump()['apellido']
                Usuarios[index]['direccion'] = updateUser.model_dump()['direccion']
                Usuarios[index]['telefono'] = updateUser.model_dump()['telefono']
                return {'respuesta': 'Usuario actualizado correctamente'}

            return {'respuesta': 'Usuario no encontrado'}
