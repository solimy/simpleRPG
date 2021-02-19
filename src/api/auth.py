from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Form, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from pydantic.types import UUID4
from sqlalchemy import select
import sqlalchemy
import traceback
import hashlib
import uuid
import jwt
import re

from src.settings import settings
from src.utils.log import logger
from src.db.sql import get_sql
from src.db.sql.model import Account


router = APIRouter()


@router.post("/auth/register")
async def register(username: EmailStr = Form(...), password: str = Form(...), alias: str = Form(...)):
    salt = uuid.uuid4().bytes
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt).digest()
    account = Account(
        id=uuid.uuid4().bytes,
        alias=alias,
        username=username,
        password=hashed_password,
        salt=salt
    )
    sql = await get_sql()
    sql.add(account)
    try:
        await sql.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already used")
    except sqlalchemy.exc.DataError as e:
        if match:=re.search('Data too long for column \'(.*)\'', e.args[0]):
            detail = f'{match.groups()[0]} is too long'
        else:
            detail = None
        raise HTTPException(status_code=400, detail=detail)
    except Exception as e:
        logger.critical(type(e))
        logger.critical(traceback.format_exc())
        raise HTTPException(status_code=500)
    finally:
        await sql.close()


class AuthenticateResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str = None

@router.post("/auth/authenticate", response_model=AuthenticateResponse)
async def authenticate(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    sql = await get_sql()
    account = (await sql.execute(select(Account).where(Account.username == data.username))).scalar()
    await sql.close()
    if not account or not hashlib.sha512(data.password.encode('utf-8') + account.salt).digest() == account.password:
        raise HTTPException(status_code=400, detail="Wrong credentials")
    return AuthenticateResponse(
        access_token=jwt.encode(
            {
                'sub': account.id.hex(),
                'exp': datetime.utcnow() + timedelta(1)
            },
            settings.jwt_secret,
            algorithm="HS256"
        ),
    )
