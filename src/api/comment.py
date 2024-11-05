from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/post/comment")
def post_comment(user_id: int, recipe_id: int, comment: str):
    with db.engine.begin() as connection:
        comment_id = connection.execute(sqlalchemy.text("INSERT INTO comments (user_id, recipe_id, comment) VALUES (:temp_user, :temp_recipe, :temp_comment) RETURNING comment_id"), 
                           {"temp_user": user_id, "temp_recipe": recipe_id, "temp_comment": comment}).fetchone()[0]
    return {"comment_id": comment_id}
