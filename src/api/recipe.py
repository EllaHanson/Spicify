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

@router.post("/post/recipe")
def post_recipe(new_recipe: recipe, user_id: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO recipes (type, title, time_needed, author_id, complexity, is_public) VALUES (:temp_type, :temp_title, :temp_time, :temp_author, :temp_complexity, :temp_public)"),
                            {"temp_type": new_recipe.type, "temp_title": new_recipe.title, "temp_time": new_recipe.time, "temp_author": user_id, "temp_complexity": new_recipe.complexity, "temp_public": new_recipe.is_public})
        
        for n in new_recipe.ingredients:
            print(n)
    return "OK"
