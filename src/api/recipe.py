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

class User(BaseModel):
    name: str
    email: str
    password: str

@router.post("/post/user")
def add_user(new_user: User):
    with db.engine.begin() as connection:
        print(f"insert user {new_user.name}")
        connection.execute(sqlalchemy.text("INSERT INTO users (username, email, password) VALUES (:new_name, :new_email, :new_password)"), 
                           {"new_name": new_user.name, "new_email": new_user.email, "new_password": new_user.password})
    return "OK"
"""
@router.post("/loggin")
def logg_in_out(user_id: int):
     with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(""))

        """




"""@router.post("/user/add")
def add_user(new_user: user):"""
    
