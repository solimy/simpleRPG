from fastapi import APIRouter, Depends

from src.settings import settings
from src.utils.log import logger
from src.utils.auth import verify_token
from src.db.redis_client import client as redis

router = APIRouter()

@router.get("/player/create", dependencies=[Depends(verify_token)])
async def create(name: str):
    return {}


@router.get("/player/load")
async def load():
    return {}


@router.get("/player/save")
async def save():
    return {}