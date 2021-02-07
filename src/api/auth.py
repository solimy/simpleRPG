from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt

from src.settings import settings
from src.utils.log import logger


router = APIRouter()

def register():
    pass


class Authenticate(BaseModel):
    username: str
    password: str

@router.post("/auth/authenticate")
def authenticate(data: OAuth2PasswordRequestForm = Depends()):
    logger.info(data)
    return {
        "token_type": "bearer",
        "access_token": jwt.encode(
            {
                'username': data.username,
                'exp': datetime.utcnow() + timedelta(1)
            },
            settings.jwt_secret,
            algorithm="HS256")
    }
