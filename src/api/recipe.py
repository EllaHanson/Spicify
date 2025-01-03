from fastapi import APIRouter, Depends, HTTPException, Response, Query
from pydantic import BaseModel
from . import auth
from typing import Optional, List, Literal

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

@router.delete("/delete/tables")
def reset():
    with db.engine.begin() as connection:
        print("resetting tables...")
        """
        connection.execute(sqlalchemy.text("DELETE FROM comments"))
        connection.execute(sqlalchemy.text("DELETE FROM favorites"))
        connection.execute(sqlalchemy.text("DELETE FROM ingredients"))
        connection.execute(sqlalchemy.text("DELETE FROM profile_info"))
        connection.execute(sqlalchemy.text("DELETE FROM recipes"))
        connection.execute(sqlalchemy.text("DELETE FROM user_tags"))
        connection.execute(sqlalchemy.text("DELETE FROM recipe_tags"))
        connection.execute(sqlalchemy.text("DELETE FROM users"))
        """
        
    return "OK"

@router.delete("/delete/recipe")
def delete_recipe(recipe_id: int):
    with db.engine.begin() as connection:
        
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM recipes WHERE recipe_id = :id"), {"id": recipe_id}).fetchone().count

        if not in_table:
            print("recipe id does not exist")
            raise HTTPException(status_code = 400, detail = "Recipe id does not exist")
                
        connection.execute(sqlalchemy.text("DELETE FROM recipes WHERE recipe_id = :id"), {"id": recipe_id})
        connection.execute(sqlalchemy.text("DELETE FROM ingredients WHERE recipe_id = :id"), {"id": recipe_id})
        connection.execute(sqlalchemy.text("DELETE FROM recipe_tags WHERE recipe_id = :id"), {"id": recipe_id})

    return Response(content = "Recipe Delete Successful", status_code = 200, media_type="text/plain")

@router.post("/post/recipe")
def post_recipe(user_id: int, title: str, type: Literal["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"], time: int, complexity: Literal["Beginner", "Homecook", "Intermetiate", "Chef"], is_public: bool, ingredients: list[ingredient], tags: Optional[List[str]] = Query(default=None)):
    with db.engine.begin() as connection:
        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count

        if not in_table:
            print("user id does not exist")
            raise HTTPException(status_code = 400, detail = "User id does not exist")

        print("inserting recipe...")
        recipe_id = connection.execute(sqlalchemy.text("""
            INSERT INTO recipes (type, title, time_needed, author_id, complexity, is_public) 
            VALUES (:temp_type, :temp_title, :temp_time, :temp_author, :temp_complexity, :temp_public) 
            RETURNING recipe_id
            """),{"temp_type": type, "temp_title": title, "temp_time": time, "temp_author": user_id, "temp_complexity": complexity, "temp_public": is_public}).fetchone()[0]
        
        print("inserting ingredients...")
        for n in ingredients:
            connection.execute(sqlalchemy.text("INSERT INTO ingredients (recipe_id, name, measurement_type, amount) VALUES (:temp_id, :temp_name, :temp_type, :temp_amount)"),
                            {"temp_id": recipe_id, "temp_name": n.name, "temp_type": n.measurement_type, "temp_amount": n.measurement_amount})
            
        print("inserting tags...")
        for n in tags:
            connection.execute(sqlalchemy.text("INSERT INTO recipe_tags (recipe_id, tag) VALUES (:temp_id, :temp_tag)"), {"temp_id": recipe_id, "temp_tag": n})

    return {"recipe_id": recipe_id}

@router.get("/get/recipe")
def get_recipe(tags: Optional[List[str]] = Query(default=None), recipe_type: Optional[str] = None, ingredients: Optional[List[str]] = Query(default=None), max_time: Optional[int] = None, chef_level: Optional[str] = None):
    return_list = []
    tag_result = []
    ingredient_result = []

    if tags:
        tag_count = len(tags)
        tags_param = ""
        tags_dict = {}
        tags_dict["tag_count"] = tag_count
        for i in range(tag_count):
            temp_tag = f"tag{i}"
            tags_param = tags_param + ":" +temp_tag
            tags_dict[temp_tag] = tags[i]
            if i < len(tags) - 1:
                tags_param = tags_param + ", "

        search_str = "SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag IN (" + tags_param + ") GROUP BY recipe_id HAVING COUNT(DISTINCT tag) = :tag_count"

        with db.engine.begin() as connection:
            tag_result = connection.execute(sqlalchemy.text(search_str), tags_dict).fetchall()

    if ingredients:
        ing_count = len(ingredients)
        ing_param = ""
        ing_dict = {}
        ing_dict["ing_count"] = ing_count
        for i in range(ing_count):
            ing_tag = f"ing{i}"
            ing_param = ing_param + ":" + ing_tag
            ing_dict[ing_tag] = ingredients[i]
            if i < len(ingredients) - 1:
                ing_param = ing_param + ", "
        
        search_str = "SELECT DISTINCT recipe_id FROM ingredients WHERE name IN (" + ing_param + ") GROUP BY recipe_id HAVING COUNT(DISTINCT ingredient_id) = :ing_count"
        print (search_str)
        print (ing_dict)
        with db.engine.begin() as connection:
            ingredient_result = connection.execute(sqlalchemy.text(search_str), ing_dict).fetchall()
    
    recipe_set = set()
    tag_set = set()
    ing_set = set()

    for recipe in tag_result:
        tag_set.add(recipe.recipe_id)
    for recipe in ingredient_result:
        ing_set.add(recipe.recipe_id)
    
    if tags is not None and ingredients is not None:
        recipe_set = tag_set & ing_set
    elif tags is not None:
        recipe_set = tag_set
    elif ingredients is not None:
        recipe_set = ing_set
        

    if recipe_type is not None or max_time is not None or chef_level is not None:
        misc_dict = {}
        search_str = "SELECT recipe_id FROM recipes WHERE "

        if recipe_type:
            search_str += "type = :recipe_type "
            misc_dict['recipe_type'] = recipe_type

            if max_time or chef_level:
                search_str += "and "
        if max_time:
            search_str += "time_needed < :time "
            misc_dict['time'] = max_time
            if chef_level:
                search_str += "and "
        if chef_level:
            search_str += "complexity = :level "
            misc_dict['level'] = chef_level
        #search_str += "LIMIT 15"

        with db.engine.begin() as connection:
            misc_result = connection.execute(sqlalchemy.text(search_str), misc_dict).fetchall()
            misc_set = set()

            for recipe in misc_result:
                misc_set.add(recipe.recipe_id)
            
        if tags is not None or ingredients is not None:
            recipe_set = recipe_set & misc_set
        else:
            recipe_set = misc_set

    return {"recipes": recipe_set}

@router.get("/get/print/recipe")
def print_recipe(recipe_id: int):

    recipe_dict = {}
    tags_list = []
    ing_list = []

    with db.engine.begin() as connection:
        recipe = connection.execute(sqlalchemy.text("""SELECT r.type, r.title, r.time_needed, u.username, r.complexity, r.rating, r.rating_count
                                                        FROM recipes r
                                                        JOIN users u ON r.author_id = u.user_id
                                                        WHERE (r.recipe_id = :recipe_id) AND (r.author_id = u.user_id)"""), {"recipe_id": recipe_id}).fetchall()

        ingredients = connection.execute(sqlalchemy.text("""SELECT CONCAT(amount, ' ', measurement_type, ' ', name) AS ing
                                                            FROM ingredients
                                                            WHERE recipe_id = :recipe_id"""), {"recipe_id": recipe_id}).fetchall()
        
        tags = connection.execute(sqlalchemy.text("""SELECT tag
                                                     FROM recipe_tags
                                                     WHERE recipe_id = :recipe_id"""), {"recipe_id": recipe_id}).fetchall()
        
    
    if recipe:
        recipe_dict['Title'] = recipe[0].title
        recipe_dict['Type'] = recipe[0].type
        recipe_dict['Time Needed'] = recipe[0].time_needed
        recipe_dict['Author'] = recipe[0].username
        recipe_dict['Complexity'] = recipe[0].complexity
        recipe_dict['Rating'] = recipe[0].rating
        recipe_dict['Rating Count'] = recipe[0].rating_count

    if ingredients:
        for i in ingredients:
            ing_list.append({i.ing})

    recipe_dict['ingredients'] = ing_list

    if tags:
        for t in tags:
            tags_list.append({t.tag})

    recipe_dict['tags'] = tags_list

    return {"Recipe": recipe_dict}

@router.get("/get/mealplan")
def meal_plan(user_id: int):
    # beginner -> homecook -> intermediate -> chef
    with db.engine.begin() as connection:

        in_table = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM users WHERE user_id = :id"), {"id": user_id}).fetchone().count

        if not in_table:
            print("user id does not exist")
            raise HTTPException(status_code = 400, detail = "User id does not exist")

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
        fav_count = len(favorites)
        
        user_tags = connection.execute(sqlalchemy.text(
            """
            SELECT tag from user_tags
            WHERE user_id = :id
            """
            ), {"id": user_id}).fetchall()
        tag_count = len(user_tags)
        
        if not favorites:
            print("No favorites! Favorite some recipes to get a meal plan")
            return(return_list)
        
        IngList = []
        TagList = []
        while favorites:
            IngList.append(favorites.pop()[0])
        while user_tags:
            TagList.append(user_tags.pop()[0])
        
        recipes1 = []
        if fav_count > 0:
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
                ), {"list": tuple(IngList)}).fetchall()
        
        recipes2 = []
        if tag_count > 0:
            recipes2 = connection.execute(sqlalchemy.text(
                """
                SELECT 
                    recipes.recipe_id AS recipe_id,
                    recipes.type AS MealType,
                    recipes.title AS RecipeName
                FROM recipes
                JOIN recipe_tags ON recipes.recipe_id = recipe_tags.recipe_id
                WHERE recipe_tags.tag IN :list
                """
                ), {"list": tuple(TagList)}).fetchall()
        
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
        print(plan)

        breakfast_in = False
        lunch_in = False
        dinner_in = False
        dessert_in = False

        for n in plan:
            type = n.type.lower()
            if type == 'breakfast' and breakfast_in == False:
                breakfast_in = True
                breakfast = {"Meal": 'Breakfast', "RecipeName": n.title, "Id": n.recipe_id}
            if type == 'lunch' and lunch_in == False:
                lunch_in = True
                lunch = {"Meal": 'Lunch', "RecipeName": n.title, "Id": n.recipe_id}
            if type == 'dinner' and dinner_in == False:
                dinner_in = True
                dinner = {"Meal": 'Dinner', "RecipeName": n.title, "Id": n.recipe_id}
            if type == 'dessert' and dessert_in == False:
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
            return_list.append({"Meal": 'Dinner', "RecipeName": 'no dinner based favorites and tags', "Id": -1})
        
        if dessert_in:
            return_list.append(dessert)
        else:
            return_list.append({"Meal": 'Dessert', "RecipeName": 'no dessert based favorites and tags', "Id": -1})

        for n in return_list:
            print(n)


        return(return_list)