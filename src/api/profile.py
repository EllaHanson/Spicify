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
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE email = :check_email"), {"check_email": new_user.email}).fetchone().count

        if in_table:
            print(f"{new_user.name} already in customer table")
            return "OK"
        
        print(f"insert user {new_user.name}")
        id = connection.execute(sqlalchemy.text("INSERT INTO users (username, email, password) VALUES (:new_name, :new_email, :new_password) RETURNING user_id"), {"new_name": new_user.name, "new_email": new_user.email, "new_password": new_user.password}).fetchone()[0]
        connection.execute(sqlalchemy.text("INSERT INTO profile_info VALUES (:temp_id)"), {"temp_id": id})

    return {"user_id": id}

@router.post("/loggin")
def loggin(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggin for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = TRUE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "OK"

@router.post("/profile")
def update_profile(id: int, level: str, about_me: str):
    with db.engine.begin() as connection:
        print(f"updating user {id} profile...")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET level = :temp_level, about_me = :temp_about WHERE user_id = :temp_id"), {"temp_level": level, "temp_about": about_me, "temp_id": id})
    return "OK"


@router.post("/loggout")
def loggout(user_id: int):
    with db.engine.begin() as connection:
        print(f"loggout for user {user_id}")
        connection.execute(sqlalchemy.text("UPDATE profile_info SET logged_in = FALSE WHERE user_id = :temp_id"), {"temp_id": user_id})
    return "OK"

    
# recipe functions

class ingredient(BaseModel):
    name: str
    measurement_type: str
    measurement_amount: int

class recipe(BaseModel):
    title: str
    type: str
    time: int
    complexity: str
    is_public: bool
    ingredients: list[ingredient]
    tags: list[str]

@router.post("/post/recipe")
def post_recipe(new_recipe: recipe, user_id: int):
    with db.engine.begin() as connection:
        print("inserting recipe...")
        recipe_id = connection.execute(sqlalchemy.text("INSERT INTO recipes (type, title, time_needed, author_id, complexity, is_public) VALUES (:temp_type, :temp_title, :temp_time, :temp_author, :temp_complexity, :temp_public) RETURNING recipe_id"),
                            {"temp_type": new_recipe.type, "temp_title": new_recipe.title, "temp_time": new_recipe.time, "temp_author": user_id, "temp_complexity": new_recipe.complexity, "temp_public": new_recipe.is_public}).fetchone()[0]
        
        print("inserting ingredients...")
        for n in new_recipe.ingredients:
            connection.execute(sqlalchemy.text("INSERT INTO ingredients (recipe_id, name, measurement_type, amount) VALUES (:temp_id, :temp_name, :temp_type, :temp_amount)"),
                            {"temp_id": recipe_id, "temp_name": n.name, "temp_type": n.measurement_type, "temp_amount": n.measurement_amount})
            
        print("inserting tags...")
        for n in new_recipe.tags:
            connection.execute(sqlalchemy.text("INSERT INTO tags (recipe_id, tag) VALUES (:temp_id, :temp_tag)"), {"temp_id": recipe_id, "temp_tag": n})

    return "OK"

@router.post("/get/filter")
def get_recipe(tags: str):
    with db.engine.begin() as connection:
        tag_result = connection.execute(sqlalchemy.text("SELECT DISTINCT recipe_id FROM tags WHERE tag = :temp_tag"), {"temp_tag": tags}).fetchall()
        print(tag_result)

        search_str = "SELECT * FROM recipes WHERE "
        while tag_result:
            temp_id = tag_result.pop()
            search_str += "recipe_id = "
            search_str += str(temp_id.recipe_id)
            if tag_result:
                search_str += " or "
        recipe_result = connection.execute(sqlalchemy.text(search_str)).fetchall()
        for n in recipe_result:
            print(n)


    # try for search with multiple tags
"""
    return_list = []
    
    if not tags:
        return return_list
    
    search_str = "SELECT recipe_id, count(tag) FROM tags WHERE "
    while tags:
        temp_tag = tags.pop()
        search_str += "tag = '"
        search_str += temp_tag
        search_str += "'"
        if tags:
            search_str += " and "
    
    search_str += "GROUP BY recipe_id"
    

    with db.engine.begin() as connection:
        tag_result = connection.execute(sqlalchemy.text(search_str)).fetchall()
        print(tag_result)
        """
    



