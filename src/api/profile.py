from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    name: str
    email: str
    password: str

@router.post("/post/user")
def add_user(new_user: User):
    with db.engine.begin() as connection:
        email_in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE email = :check_email"), {"check_email": new_user.email}).fetchone().count
        name_in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE username = :check_name"), {"check_name": new_user.name}).fetchone().count

        if email_in_table:
            print(f"email already used")
            return "OK"
        if name_in_table:
            print("username already taken, try another")
            return "OK"
        
        print(f"inserting user {new_user.name}...")

        id = connection.execute(sqlalchemy.text(
                """
                INSERT INTO users 
                    (username, email, password) 
                VALUES (:new_name, :new_email, :new_password) 
                RETURNING user_id
                """), {"new_name": new_user.name, "new_email": new_user.email, "new_password": new_user.password}).fetchone()[0]
        
        connection.execute(sqlalchemy.text("INSERT INTO profile_info VALUES (:temp_id)"), {"temp_id": id})

    return {"user_id": id}

@router.post("/loggin")
def loggin(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggin for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = TRUE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "Login successful!"

@router.put("/profile")
def update_profile(id: int, level: str, about_me: str, username: str, user_id: int):
    with db.engine.begin() as connection:
        print(f"updating user {id} profile...") 
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count

        if in_table:
            print(f"user id ({user_id}) not found")

        connection.execute(sqlalchemy.text("UPDATE profile_info SET level = :temp_level, about_me = :temp_about WHERE user_id = :temp_id"), {"temp_level": level, "temp_about": about_me, "temp_id": id})
        connection.execute(sqlalchemy.text("UPDATE users SET username = :temp_user WHERE user_id = :userid"), {"temp_user": username, "userid": user_id})
    return "Profile updated successfully!"

@router.post("/loggout")
def loggout(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggout for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = FALSE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "Logout successful!"

