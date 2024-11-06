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
def get_recipe(tags: list[str] = None, recipe_type: str = None, ingredients: list[str] = None, max_time: int = None, chef_level: str = None):

    return_list = []
    tag_count = len(tags)
    ing_count = len(ingredients)

    if tags:
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

        with db.engine.begin() as connection:
            tag_result = connection.execute(sqlalchemy.text(search_str)).fetchall()

            if tag_result:
                search_str = "SELECT * FROM recipes WHERE "
                while tag_result:
                    temp_id = tag_result.pop()
                    search_str += "recipe_id = "
                    search_str += str(temp_id.recipe_id)
                    if tag_result:
                        search_str += " or "
                recipe_tag_result = connection.execute(sqlalchemy.text(search_str)).fetchall()
    else: 
        recipe_tag_result = []
    
    if ingredients:

        search_str = "SELECT DISTINCT recipe_id FROM ingredients WHERE name IN ("
        while ingredients:
            temp_ing = ingredients.pop()
            search_str += "'"
            search_str += temp_ing
            search_str += "'"
            if ingredients:
                search_str += ", "
    
        search_str += ") GROUP BY recipe_id HAVING COUNT(DISTINCT name) = "
        search_str += str(ing_count)

        with db.engine.begin() as connection:
            ingredient_result = connection.execute(sqlalchemy.text(search_str)).fetchall()

            if ingredient_result :
                search_str = "SELECT * FROM recipes WHERE "
                while ingredient_result:
                    temp_id = ingredient_result.pop()
                    search_str += "recipe_id = "
                    search_str += str(temp_id.recipe_id)
                    if ingredient_result:
                        search_str += " or "
                recipe_ingredients_result = connection.execute(sqlalchemy.text(search_str)).fetchall()

    # intersect of tags results and ingredient results
    if tag_count > 0 and ing_count > 0:
        recipe_middle_list = list(set(recipe_tag_result) & set(recipe_ingredients_result))
    elif tag_count > 0:
        recipe_middle_list = recipe_tag_result
    elif ing_count > 0:
        recipe_middle_list = recipe_ingredients_result
    else:
        recipe_middle_list = []
        
    rest_count = False
    if recipe_type or max_time or chef_level:
        rest_count = True

        search_str = "SELECT recipe_id FROM recipes WHERE "

        if recipe_type:
            search_str += "type = '"
            search_str += recipe_type
            search_str += "' "
            if max_time or chef_level:
                search_str += "and "
        if max_time:
            search_str += "time_needed < "
            search_str += str(max_time)
            search_str += " "
            if chef_level:
                search_str += "and "
        if chef_level:
            search_str += "complexity = '"
            search_str += chef_level
            search_str += "' "


        search_str += "and is_public = TRUE"
        with db.engine.begin() as connection:
            rest_result = connection.execute(sqlalchemy.text(search_str)).fetchall()

            if rest_result :
                search_str = "SELECT * FROM recipes WHERE "
                while rest_result:
                    temp_id = rest_result.pop()
                    search_str += "recipe_id = "
                    search_str += str(temp_id.recipe_id)
                    if rest_result:
                        search_str += " or "
                recipe_rest_result = connection.execute(sqlalchemy.text(search_str)).fetchall()

    if (tag_count > 0 or ing_count > 0) and rest_count:
        recipe_list = list(set(recipe_middle_list) & set(recipe_rest_result))
    elif (tag_count > 0 or ing_count > 0):
        recipe_list = recipe_middle_list
    elif rest_count:
        recipe_list = recipe_rest_result
    else:
        recipe_list = []
    
    return_list = []
    for n in recipe_list:
        print(n.title)
        return_list.append(n.recipe_id)


    return return_list

        
    




