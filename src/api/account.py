from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
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
from src.db.sql import get_sql, model as sql_model
from src.db.redis import get_redis, model as redis_model


router = APIRouter()


@router.post("/account/register")
async def register(username: EmailStr = Form(...), password: str = Form(...), alias: str = Form(...)):
    salt = uuid.uuid4().bytes
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt).digest()
    account = sql_model.Account(
        id=uuid.uuid4().bytes,
        alias=alias,
        username=username,
        password=hashed_password,
        salt=salt
    )
    entity = sql_model.Entity(
        id=uuid.uuid4().bytes,
        account_id=account.id,
    )
    position = sql_model.Position(
        id=entity.id,
        location='default',
        x=0,
        y=0,
        z=0,
    )
    try:
        sql_session = await get_sql()
        sql_session.add(account)
        await sql_session.flush()
        sql_session.add(entity)
        await sql_session.flush()
        sql_session.add(position)
        await sql_session.commit()
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
        await sql_session.rollback()
        raise HTTPException(status_code=status_code, detail=detail)
    finally:
        await sql_session.close()


class AuthenticateResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str = None

@router.post("/account/authenticate", response_model=AuthenticateResponse)
async def authenticate(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    try:
        sql_session = await get_sql()
        account = (await sql_session.execute(
            select(sql_model.Account)
            .where(sql_model.Account.username == data.username)
        )).scalar()
        if not account:
            logger.error(f'account "{data.username}" not registered')
            raise HTTPException(status_code=400, detail="Wrong credentials")
        elif not hashlib.sha512(data.password.encode('utf-8') + account.salt).digest() == account.password:
            logger.error(f'({data.username}) wrong password')
            raise HTTPException(status_code=400, detail="Wrong credentials")
        entity = (await sql_session.execute(
            select(sql_model.Entity)
            .where(sql_model.Entity.account_id == account.id)
        )).scalar()
        position = (await sql_session.execute(
            select(sql_model.Position)
            .where(sql_model.Position.id == entity.id)
        )).scalar()
        redis_client = await get_redis()
        rentity = redis_model.Entity(redis_client, entity.id)
        await rentity.set_alias(account.alias)
        rposition = redis_model.Position(redis_client, entity.id)
        await rentity.set_alias(account.alias)
    finally:
        await sql_session.close()
    return AuthenticateResponse(
        access_token=jwt.encode(
            {
                'sub': account.username,
                'exp': datetime.utcnow() + timedelta(1),
                'eid': entity.id.hex(),
            },
            settings.jwt_secret,
            algorithm="HS256"
        ),
    )
