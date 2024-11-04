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
def get_recipe(tags: list[str]):

    return_list = []
    
    if tags:
    
        tag_count = len(tags)
    
        search_str = "SELECT DISTINCT recipe_id FROM tags WHERE tag IN ("
        while tags:
            temp_tag = tags.pop()
            search_str += "'"
            search_str += temp_tag
            search_str += "'"
            if tags:
                search_str += ", "
    
        search_str += ") GROUP BY recipe_id HAVING COUNT(DISTINCT tag) = "
        search_str += str(tag_count)
        print(search_str)

        with db.engine.begin() as connection:
            tag_result = connection.execute(sqlalchemy.text(search_str)).fetchall()
            print(tag_result)

            search_str = "SELECT * FROM recipes WHERE "
            while tag_result:
                temp_id = tag_result.pop()
                search_str += "recipe_id = "
                search_str += str(temp_id.recipe_id)
                if tag_result:
                    search_str += " or "
            recipe_result = connection.execute(sqlalchemy.text(search_str)).fetchall()
        

    return "OK"

        
    




