from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from pydantic import BaseModel
from loguru import logger
from sqlalchemy import select, func
import sqlalchemy
import traceback
import uuid
import jwt
import re

from src.utils.auth import OAuth2Token


router = APIRouter()


@router.post("/game/character/image/set")
async def set_image(token: str = Depends(OAuth2Token()), image: UploadFile = File(...)):
    pass
