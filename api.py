from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from app.routers import user


app = FastAPI()

app.include_router(user.router)

