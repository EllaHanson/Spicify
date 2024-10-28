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
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE email = :check_email"), {"check_email": new_user.email}).fetchone().count

        if in_table:
            print(f"{new_user.name} already in customer table")
            return "OK"
        
        print(f"insert user {new_user.name}")
        connection.execute(sqlalchemy.text("INSERT INTO users (username, email, password) VALUES (:new_name, :new_email, :new_password)"), {"new_name": new_user.name, "new_email": new_user.email, "new_password": new_user.password})
    return "OK"

@router.post("/loggin")
def loggin(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggin for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE users SET logged_in = TRUE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "OK"

@router.post("/loggout")
def loggout(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggout for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE users SET logged_in = FALSE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "OK"

    
