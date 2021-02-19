from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from pydantic import BaseModel
from loguru import logger
from sqlalchemy import select, func
import sqlalchemy
import traceback
import uuid
import re

from src.db.sql.model import Entity, Character
from src.utils.auth import OAuth2Token
from src.settings import settings
from src.db.sql import get_sql


router = APIRouter()


class MaxCharCountReached(Exception): pass


class CreateRequest(BaseModel):
    name: str


@router.post("/game/character/create")
async def create(token: str = Depends(OAuth2Token()), data: CreateRequest = Depends()):
    id = uuid.uuid4().bytes
    account_id = uuid.UUID(token['sub']).bytes
    entity = Entity(
        id=id,
        account_id=account_id,
    )
    character = Character(
        id=entity.id,
        name=data.name,
    )
    try:
        sql = await get_sql()
        if (await sql.execute(
            select(func.count(Entity.id))
            .where(Entity.account_id == account_id)
            .join(Character, Entity.id == Character.id)
            )).scalar() >= settings.max_character_by_account:
            raise MaxCharCountReached()
        sql.add(entity)
        await sql.flush()
        sql.add(character)
        await sql.commit()
    except Exception as e:
        if isinstance(e, sqlalchemy.exc.IntegrityError) and (
            match := re.search(f'Duplicate entry \'(.*)\' for key \'character.name\'', e.args[0])):
            detail = f'character name "{match.groups()[0]}" already used'
            status_code = 400
            logger.error(detail)
        elif isinstance(e, sqlalchemy.exc.DataError) and (
            match := re.search('Data too long for column \'(.*)\'', e.args[0])):
            detail = f'{match.groups()[0]} is too long'
            status_code = 400
            logger.error(detail)
        elif isinstance(e, MaxCharCountReached):
            detail = f'maximum characters count by account reached ({settings.max_character_by_account})'
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


# @router.post("/game/character/image/set")
# async def set_image(token: str = Depends(OAuth2Token()), image: UploadFile = File(...)):
#     pass
