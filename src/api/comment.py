from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/comment")
def post_comment():
    return "OK"