from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

#added for version 1
import sqlalchemy
from src import database as db
#import src
#till here


router = APIRouter(
    prefix="/recipe",
    tags=["recipe"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/deliver/{order_id}")
def post_recipe():

    print("hi")
    return "OK"
