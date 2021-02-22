from typing import Dict, Optional
from starlette.requests import Request
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.settings import settings


class OAuth2Token(OAuth2PasswordBearer):
    def __init__(self):
        super().__init__(tokenUrl='account/authenticate')

    async def __call__(self, request: Request) -> Optional[Dict]:
        token = await super().__call__(request)
        try:
            token = jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])
        except:
            raise HTTPException(status_code=400, detail="JWT token expired")
        return token
