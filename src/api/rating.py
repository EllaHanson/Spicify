from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/rating",
    tags=["rating"],
    dependencies=[Depends(auth.get_api_key)],
)

class Rating(BaseModel):
    recipe_id: str
    rating: int

@router.post("/post/rating")
def post_rating(recipe_id: str, rating: int):

    # calculates the new rating by: (overall rating * amount of ratings + recent rating) / (amount of ratings + 1)
    recipe_rating_sql = """UPDATE recipes SET rating = 
                            ROUND((CAST(rating as numeric) * rating_count + :rating)/ (rating_count + 1), 1),
                            rating_count = rating_count + 1
                            WHERE recipe_id = :recipe_id"""
    
    recipe_name_sql = "SELECT title FROM recipes WHERE recipe_id = :recipe_id"
    with db.engine.begin() as connection:
        recipe_rating = connection.execute(sqlalchemy.text(recipe_rating_sql), 
                                        {"rating": rating, "recipe_id": recipe_id})
        recipe_name = connection.execute(sqlalchemy.text(recipe_name_sql), {"recipe_id": recipe_id}).scalar()

    print(f"\"{recipe_name}\" has been given a rating of {rating} / 5")
    return "OK"
