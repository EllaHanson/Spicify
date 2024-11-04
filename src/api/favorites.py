from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/favorite")
def post_favorite():
    return "OK"