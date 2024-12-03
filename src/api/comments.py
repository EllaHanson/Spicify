from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/comments",
    tags=["comment"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/comments")
def post_comment(user_id: int, recipe_id: int, comment: str):
    with db.engine.begin() as connection:

        #check if user id exists
        user_exists = connection.execute(sqlalchemy.text("SELECT 1 FROM users WHERE user_id = :user_id"), {"user_id": user_id}).fetchone()        
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found!")
        
        #check if recipe exists
        recipe_exists = connection.execute(sqlalchemy.text("SELECT 1 FROM recipes WHERE recipe_id = :recipe_id"), {"recipe_id": recipe_id}).fetchone()
        if not recipe_exists:
            raise HTTPException(status_code=404, detail="Recipe not found!")

        comment_id = connection.execute(sqlalchemy.text("INSERT INTO comments (user_id, recipe_id, comment) VALUES (:temp_user, :temp_recipe, :temp_comment) RETURNING comment_id"), 
                           {"temp_user": user_id, "temp_recipe": recipe_id, "temp_comment": comment}).fetchone()[0]
    return {"comment_id": comment_id}