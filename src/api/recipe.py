from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/recipe",
    tags=["recipe"],
    dependencies=[Depends(auth.get_api_key)],
)

class user:
    name: str
    email: str
    password: str

@router.post("/post")
def post_recipe():

    print("hi")
    return "OK"



"""@router.post("/user/add")
def add_user(new_user: user):"""
    
