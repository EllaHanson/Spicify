from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/update",
    tags=["update"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/profile")
def update_profile():
    return "OK"