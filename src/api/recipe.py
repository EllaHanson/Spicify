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

class user(BaseModel):
    name: str
    email: str
    password: str

@router.post("/post")
def post_recipe(new_user: user):


    with db.engine.begin() as connection:
        print(f"insert user {user.name}")
        connection.execute(sqlalchemy.text("INSERT INTO users (username, email, password) VALUES :new_name, :new_email, :new_password"), 
                           {"new_name": user.name, "new_email": user.email, "new_password": user.password})
    return "OK"



"""@router.post("/user/add")
def add_user(new_user: user):"""
    
