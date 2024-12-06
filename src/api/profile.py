from fastapi import APIRouter, Depends, HTTPException, Response, Query
from pydantic import BaseModel
from . import auth
from typing import Optional, List

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    name: str
    email: str
    password: str

@router.delete("/delete/profile")
def delete_user(user_id: int):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count

        if not in_table:
            print("user id does not exist")
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        connection.execute(sqlalchemy.text("DELETE FROM users WHERE user_id = :id"), {"id": user_id})
        connection.execute(sqlalchemy.text("DELETE FROM user_tags WHERE user_id = :id"), {"id": user_id})
        connection.execute(sqlalchemy.text("DELETE FROM profile_info WHERE user_id = :id"), {"id": user_id})

    return Response(content = "User Delete Successful", status_code = 200, media_type="text/plain")

@router.get("/get/user/info")
def return_user(user_id: int):
     with db.engine.begin() as connection:
        user_info = connection.execute(sqlalchemy.text("SELECT username, email, created_at FROM users WHERE user_id = :id"), {"id": user_id}).fetchone()
        user_tags = connection.execute(sqlalchemy.text("SELECT tag FROM user_tags WHERE user_id = :id"), {"id": user_id}).fetchall()

        if user_info is None:
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        tags = []
        for tag in user_tags:
            tags.append(tag.tag)

        date_time = user_info.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        return_info = {}
        return_info["username"] = user_info.username
        return_info["email"] = user_info.email
        return_info["user_since"] = date_time
        return_info["user_tags"] = tags
        
        return return_info


@router.post("/post/user")
def add_user(name: str, email: str, password: str):
    with db.engine.begin() as connection:
        email_in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE email = :check_email"), {"check_email": email}).fetchone().count
        name_in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE username = :check_name"), {"check_name": name}).fetchone().count

        if email_in_table:
            print(f"email already used")
            raise HTTPException(status_code = 400, detail = "Email already exists for other profile")
            
        if name_in_table:
            print("username already taken, try another")
            raise HTTPException(status_code = 400, detail = "Username already used for other profile")
        
        print(f"inserting user {name}...")

        id = connection.execute(sqlalchemy.text(
                """
                INSERT INTO users 
                    (username, email, password) 
                VALUES (:new_name, :new_email, :new_password) 
                RETURNING user_id
                """), {"new_name": name, "new_email": email, "new_password": password}).fetchone()[0]
        
        connection.execute(sqlalchemy.text("INSERT INTO profile_info VALUES (:temp_id)"), {"temp_id": id})

    return {"user_id": id}

@router.put("/put/loggin")
def loggin(user_id: int, password: str):
    with db.engine.begin() as connection:
        name_in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :check_name"), {"check_name": user_id}).fetchone().count

        if not name_in_table:
            print("user id not registered, can't loggin")
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        table_password = connection.execute(sqlalchemy.text("SELECT password FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().password
        
        if table_password == password:
            print(f"loggin for user {user_id}")
            connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = TRUE WHERE user_id = :temp_id"), {"temp_id": user_id})
            return Response(content = str("Loggin Successful"), status_code = 200, media_type="text/plain")
        else:
            print("Incorrect Password")
            raise HTTPException(status_code = 400, detail = "Incorrect Password")

@router.patch("/patch/profile")
def update_profile(user_id: int, level: str = None, about_me: str = None, username: str = None):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count

        if not in_table:
            print(f"user id not found")
            raise HTTPException(status_code = 400, detail = "User id does not exist")

        print(f"updating user {user_id} profile...") 

        if level is not None:
            connection.execute(sqlalchemy.text(
                """UPDATE profile_info SET level = :temp_level WHERE user_id = :temp_id"""), 
                {"temp_level": level, "temp_id": user_id})
        if about_me is not None:
            connection.execute(sqlalchemy.text(
                """UPDATE profile_info SET about_me = :temp_info WHERE user_id = :temp_id"""), 
                {"temp_info": about_me, "temp_id": user_id})

        if username is not None:
            connection.execute(sqlalchemy.text(
                """UPDATE users SET username = :temp_user WHERE user_id = :userid"""), 
                {"temp_user": username, "userid": user_id})
            
    return Response(content = "Profile Update Successful", status_code = 200, media_type="text/plain")

@router.post("/post/user/tag")
def add_user_tag(user_id: int, tag: str):
    with db.engine.begin() as connection:
        tag_id = connection.execute(sqlalchemy.text("INSERT INTO user_tags (user_id, tag) VALUES (:id, :user_tag) RETURNING tag_id"),
                            {"id": user_id, "user_tag": tag}).fetchone()
    return {"tag_id": tag_id.tag_id}


@router.put("/put/loggout")
def loggout(user_id: int):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count
        if not in_table:
            print(f"user id not found")
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        print(f"loggout for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = FALSE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return Response(content = str("Loggout Successful"), status_code = 200, media_type="text/plain")
 
