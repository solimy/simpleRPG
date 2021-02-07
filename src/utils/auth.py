from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.settings import settings
from src.utils.log import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/authenticate')

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])
    except:
        raise HTTPException(status_code=400, detail="JWT token expired")
