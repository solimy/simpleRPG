from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel
from loguru import logger
import uuid

from src.utils.auth import OAuth2Token
from src.db.sql.model import Entity
from src.db.sql.model import Character


router = APIRouter()

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
    )


@router.post("/game/character/image/set")
async def create(token: str = Depends(OAuth2Token()), image: UploadFile = File(...)):
    pass


@router.post("/test")
async def test(token: str = Depends(OAuth2Token())):
    logger.info(token)