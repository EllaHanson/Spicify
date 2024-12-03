from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/explore/favorites")
def add_favorite(user_id, recipe_id):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count
        if not in_table:
            print(f"user id not found")
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM recipes WHERE recipe_id = :id"), {"id": recipe_id}).fetchone().count
        if not in_table:
            print(f"recipe id not found")
            raise HTTPException(status_code = 400, detail = "Recipe id does not exist")

        connection.execute(sqlalchemy.text("INSERT INTO favorites (user_id, recipe_id) VALUES (:user_id, :recipe_id)"), {"user_id": user_id, "recipe_id": recipe_id})
    return "Favorite added successfully!"

@router.get("/blog/favorites")
def get_favorites(user_id):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count
        if not in_table:
            print(f"user id not found")
            raise HTTPException(status_code = 400, detail = "User id does not exist")
        
        favorites = connection.execute(sqlalchemy.text("SELECT FROM favorites WHERE user_id = :user_id"), {"user_id": user_id})
    return favorites