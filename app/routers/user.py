from fastapi import APIRouter, Depends, HTTPException
from app.schemas import User
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from typing import Annotated



router = APIRouter(
    prefix = "/user",
    tags = ['Users'] 
)

Usuarios = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users = {
    "lisa": {"username": "lisa", "email": "luisangelilozada@gmailcom", "password": "lisa25"},
    "user2": {"username": "user2", "email": "user2@gmailcom", "password": "user2"}
}

def encode_token (payload: dict)-> str:
    token = jwt .encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)])-> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@router.post("/token")

def login (form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"] :
        raise HTTPException(status_code = 400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]} )
    return { "access_token": token }

@router.get("/profile")

def profile (my_user: Annotated[dict, Depends(decode_token)]):
    return my_user

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
