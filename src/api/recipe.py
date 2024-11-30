from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth

import sqlalchemy
import random
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

@router.post("/reset/tables")
def reset():
    with db.engine.begin() as connection:
        print("resetting tables...")
        connection.execute(sqlalchemy.text("DELETE FROM comments"))
        connection.execute(sqlalchemy.text("DELETE FROM favorites"))
        connection.execute(sqlalchemy.text("DELETE FROM ingredients"))
        connection.execute(sqlalchemy.text("DELETE FROM profile_info"))
        connection.execute(sqlalchemy.text("DELETE FROM recipes"))
        connection.execute(sqlalchemy.text("DELETE FROM tags"))
        connection.execute(sqlalchemy.text("DELETE FROM users"))
    return "OK"

@router.get("/post/recipe")
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



@router.post("/post/meal_plan")
def meal_plan(user_id: int):
    # beginner -> homecook -> intermediate -> chef
    with db.engine.begin() as connection:
        return_list = []
        favorites = connection.execute(sqlalchemy.text(
            """
            SELECT 
                name as Ingredient,
                count(*) as IngCount
            FROM favorites 
            JOIN ingredients on ingredients.recipe_id = favorites.recipe_id
            WHERE user_id = :id
            GROUP BY name
            HAVING count(*) > 1
            ORDER BY count(*) desc
            """
            ), {"id": user_id}).fetchall()
        
        user_tags = connection.execute(sqlalchemy.text(
            """
            SELECT tag from user_tags
            WHERE user_id = :id
            """
            ), {"id": user_id}).fetchall()
        
        if not favorites:
            print("No favorites! Favorite some recipes to get a meal plan")
            return(return_list)
        
        IngList = []
        TagList = []
        while favorites:
            IngList.append(favorites.pop()[0])
        while user_tags:
            TagList.append(user_tags.pop()[0])
        
        
        recipes1 = connection.execute(sqlalchemy.text(
            """
            SELECT 
                recipes.recipe_id AS recipe_id,
                recipes.type AS MealType,
                recipes.title AS RecipeName
            FROM recipes
            JOIN ingredients ON recipes.recipe_id = ingredients.recipe_id
            WHERE ingredients.name IN :list
            """
            ), {"list": tuple(IngList)}
            ).fetchall()
        
        recipes2 = connection.execute(sqlalchemy.text(
            """
            SELECT 
                recipes.recipe_id AS recipe_id,
                recipes.type AS MealType,
                recipes.title AS RecipeName
            FROM recipes
            JOIN tags ON recipes.recipe_id = tags.recipe_id
            WHERE tags.tag IN :list
            """
            ), {"list": tuple(TagList)}
            ).fetchall()
        
        recipe_set = set({})
        for n in recipes1:
            recipe_set.add(n.recipe_id)
        
        for n in recipes2:
            recipe_set.add(n.recipe_id)

        plan = connection.execute(sqlalchemy.text(
            """
            SELECT 
                recipe_id,
                title, 
                LOWER(type) AS type, 
                complexity
            FROM recipes
            WHERE recipe_id IN :list
            """
            ), {"list": tuple(recipe_set)}
            ).fetchall()
        
        print("Recipe Options:")

        random.shuffle(plan)

        for n in plan:
            print(n)

        breakfast_in = False
        lunch_in = False
        dinner_in = False
        dessert_in = False

        for n in plan:
            if n.type == 'breakfast' and breakfast_in == False:
                breakfast_in = True
                breakfast = {"Meal": 'Breakfast', "RecipeName": n.title, "Id": n.recipe_id}
            if n.type == 'lunch' and lunch_in == False:
                lunch_in = True
                lunch = {"Meal": 'Lunch', "RecipeName": n.title, "Id": n.recipe_id}
            if n.type == 'Dinner' and dinner_in == False:
                dinner_in = True
                dinner = {"Meal": 'Dinner', "RecipeName": n.title, "Id": n.recipe_id}
            if n.type == 'Dessert' and dessert_in == False:
                dessert_in = True
                dessert = {"Meal": 'Dessert', "RecipeName": n.title, "Id": n.recipe_id}
            
        if breakfast_in:
            return_list.append(breakfast)
        else:
            return_list.append({"Meal": 'Breakfast', "RecipeName": 'no breakfast based favorites and tags', "Id": -1})

        if lunch_in:
            return_list.append(lunch)
        else:
            return_list.append({"Meal": 'Lunch', "RecipeName": 'no lunch based favorites and tags', "Id": -1})

        if dinner_in:
            return_list.append(dinner)
        else:
            return_list.append({"Meal": 'Lunch', "RecipeName": 'no dinner based favorites and tags', "Id": -1})
        
        if dessert_in:
            return_list.append(dessert)
        else:
            return_list.append({"Meal": 'Dessert', "RecipeName": 'no dessert based favorites and tags', "Id": -1})

        for n in return_list:
            print(n)


        return(return_list)