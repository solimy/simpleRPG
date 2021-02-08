from fastapi import APIRouter, Depends

from src.settings import settings
from src.utils.log import logger
from src.utils.auth import verify_token

router = APIRouter()


@router.get("/player/create", dependencies=[Depends(verify_token)])
def use():
    pass
