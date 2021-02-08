from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Form, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import hashlib
import uuid
import jwt

from src.settings import settings
from src.utils.log import logger
from src.db.sql import new_session as new_sql
from src.db.sql.model import User


router = APIRouter()


@router.post("/auth/register")
def register(username: EmailStr = Form(...), password: str = Form(...), alias: str = Form(...)):
    salt = uuid.uuid4().bytes
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt).digest()
    user = User(
        alias=alias,
        username=username,
        password=hashed_password,
        salt=salt
    )
    sql = new_sql()
    sql.add(user)
    try:
        sql.commit()
    except:
        raise HTTPException(status_code=400, detail="Username already used")


class AuthenticateResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str = None

@router.post("/auth/authenticate", response_model=AuthenticateResponse)
def authenticate(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    sql = new_sql()
    try:
        user = sql.query(User).filter_by(username=data.username).first()
        assert hashlib.sha512(data.password.encode('utf-8') + user.salt).digest() == user.password
    except:
        raise HTTPException(status_code=400, detail="Wrong credentials")
    return AuthenticateResponse(
        access_token=jwt.encode(
            {
                'sub': data.username,
                'exp': datetime.utcnow() + timedelta(1)
            },
            settings.jwt_secret,
            algorithm="HS256"
        ),
    )
