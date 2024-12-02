from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/explore/favorites")
def add_favorite(user_id, recipe_id):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO favorites (user_id, recipe_id) VALUES (:user_id, :recipe_id)"), {"user_id": user_id, "recipe_id": recipe_id})
    return "Favorite added successfully!"

@router.get("/blog/favorites")
def get_favorites(user_id):
    with db.engine.begin() as connection:
        favorites = connection.execute(sqlalchemy.text("SELECT FROM favorites WHERE user_id = :user_id"), {"user_id": user_id})
    return favorites