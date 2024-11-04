from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/rating",
    tags=["rating"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/rating")
def post_rating():
    return "OK"