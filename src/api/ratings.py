from fastapi import APIRouter, Depends, HTTPException, Response
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
    recipe_id: int
    rating: int

@router.post("/post/rating")
def post_rating(recipe_id: int, rating: int):

    # calculates the new rating by: (overall rating * amount of ratings + recent rating) / (amount of ratings + 1)
    recipe_rating_sql = """UPDATE recipes SET rating = 
                            ROUND((CAST(rating as numeric) * rating_count + :rating)/ (rating_count + 1), 1),
                            rating_count = rating_count + 1
                            WHERE recipe_id = :recipe_id
                            RETURNING title"""

    with db.engine.begin() as connection:
        # Checks if recipe id exists
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM recipes WHERE recipe_id = :id"), {"id": recipe_id}).fetchone().count
        if not in_table:
                return HTTPException(status_code = 400, detail = "Recipe id does not exist!")
        # This addresses the peer review feedback where rating boundaries could be broken
        elif rating > 5 or rating < 0:
            raise HTTPException(status_code = 400, detail = "Given rating breaks the boundaries!")
        else:
            recipe_rating = connection.execute(sqlalchemy.text(recipe_rating_sql), 
                                            {"rating": rating, "recipe_id": recipe_id}).scalar()

    print(f"\"{recipe_rating}\" has been given a rating of {rating} / 5")
    return Response(status_code = 200)

