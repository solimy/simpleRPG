from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Form, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from loguru import logger
import sqlalchemy
import traceback
import hashlib
import uuid
import jwt
import re

from src.settings import settings
from src.db.sql import get_sql
from src.db.sql.model import Account


router = APIRouter()


@router.post("/account/register")
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
    try:
        sql = await get_sql()
        sql.add(account)
        await sql.commit()
    except Exception as e:
        if isinstance(e, sqlalchemy.exc.IntegrityError) and (
            match := re.search(f'Duplicate entry \'(.*)\' for key \'account.username\'', e.args[0])):
            detail = f'username "{match.groups()[0]}" already used'
            status_code = 400
            logger.error(detail)
        elif isinstance(e, sqlalchemy.exc.IntegrityError) and (
            match := re.search(f'Duplicate entry \'(.*)\' for key \'account.alias\'', e.args[0])):
            detail = f'alias "{match.groups()[0]}" already used'
            status_code = 400
            logger.error(detail)
        elif isinstance(e, sqlalchemy.exc.DataError) and (
            match := re.search('Data too long for column \'(.*)\'', e.args[0])):
            detail = f'{match.groups()[0]} is too long'
            status_code = 400
            logger.error(detail)
        else:
            detail = None
            status_code = 500
            logger.critical(traceback.format_exc())
        await sql.rollback()
        raise HTTPException(status_code=status_code, detail=detail)
    finally:
        await sql.close()


class AuthenticateResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str = None

@router.post("/account/authenticate", response_model=AuthenticateResponse)
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
