from fastapi import APIRouter, Depends
from pydantic import BaseModel
from . import auth
import random
import string


import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/populate",
    tags=["populate"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.put("/rating")
def add_ratings():
    with db.engine.begin() as connection:
<<<<<<< HEAD
        for x in range(1000):
            mod1 = random.randint(5, 15)
            temp_name = ''.join(random.choices(string.ascii_letters,k=mod1))
            temp_email = temp_name
            temp_pass = temp_name
=======
        for x in range(20000):
            mod = random.randint(5, 15)
            temp_name = ''.join(random.choices(string.ascii_letters,k=mod))

            mod = random.randint(5, 15)
            temp_email = ''.join(random.choices(string.ascii_letters,k=mod))

            mod = random.randint(5, 15)
            temp_pass = ''.join(random.choices(string.ascii_letters,k=mod))
>>>>>>> e3b876efc3685e7df84e87d333fe9cde19d3f3a7

            user_id = connection.execute(sqlalchemy.text("""
                                                         INSERT INTO users (username, email, password) VALUES (:name, :e, :pass) RETURNING user_id
                                                         """), 
                                         {"name": str(temp_name), "e": str(temp_email), "pass": str(temp_pass)}).fetchone()[0]
            
            level = ["beginner", "homecook", "intermediate", "chef"]
<<<<<<< HEAD
            mod_level = random.randint(0, 3)
            temp_level = level[mod_level]
            temp_about = ''.join(random.choices(string.ascii_letters,k=mod1))
            log = True
                
=======
            mod = random.randint(0, 3)
            temp_level = level[mod]
            mod = random.randint(1, 50)
            temp_about = ''.join(random.choices(string.ascii_letters,k=mod))
            logged_in = random.randint(0,1)
            log = False
            if logged_in == 1:
                log = True
                

>>>>>>> e3b876efc3685e7df84e87d333fe9cde19d3f3a7
            connection.execute(sqlalchemy.text("""
                                               INSERT INTO profile_info (user_id, level, about_me, logged_in) VALUES (:id, :l, :a, :in)
                                               """), 
                               {'id': user_id,'l': temp_level, 'a': temp_about, 'in': log})
        



@router.post("/populate/profile")
def add_lines():
    with db.engine.begin() as connection:
        for num in range(500):
            mod = random.randint(5, 15)
            temp_name = ''.join(random.choices(string.ascii_letters,k=mod))

            mod = random.randint(5, 15)
            temp_email = ''.join(random.choices(string.ascii_letters,k=mod))

            mod = random.randint(5, 15)
            temp_pass = ''.join(random.choices(string.ascii_letters,k=mod))

            user_id = connection.execute(sqlalchemy.text("""
                                                         INSERT INTO users (username, email, password) VALUES (:name, :e, :pass) RETURNING user_id
                                                         """), 
                                         {"name": str(temp_name), "e": str(temp_email), "pass": str(temp_pass)}).fetchone()[0]
            
            level = ["beginner", "homecook", "intermediate", "chef"]
            mod = random.randint(0, 3)
            temp_level = level[mod]
            mod = random.randint(1, 50)
            temp_about = ''.join(random.choices(string.ascii_letters,k=mod))
            logged_in = random.randint(0,1)
            log = False
            if logged_in == 1:
                log = True
                

            connection.execute(sqlalchemy.text("""
                                               INSERT INTO profile_info (user_id, level, about_me, logged_in) VALUES (:id, :l, :a, :in)
                                               """), 
                               {'id': user_id,'l': temp_level, 'a': temp_about, 'in': log})
            
            user_tags = ["vegetarian", "dairy free", "gluten free", "vegan", "pescatarian", "keto", "high protein"]

            count = int(random.randint(1, 5))
            for x in range(count):
                mod = random.randint(0, 6)
                temp_tag = user_tags[mod]
                connection.execute(sqlalchemy.text("INSERT INTO user_tags (user_id, tag) VALUES (:id, :t)"), {"id": user_id, "t": temp_tag})

            count_r = int(random.randint(0, 10))
            for r in range(count_r):
                type = ["breakfast", "lunch", "dinner", "dessert"]
                temp_type = type[int(random.randint(0, 3))]

                temp_name = ''.join(random.choices(string.ascii_letters,k=int(random.randint(5, 20))))

                temp_time = int(random.randint(1, 200))

                temp_comp = level[int(random.randint(0, 3))]

                rate = random.randint(0, 5)
                r_count = random.randint(0, 1000)

                recipe_id = connection.execute(sqlalchemy.text("""
                        INSERT INTO recipes (type, title, time_needed, author_id, complexity, is_public, rating, rating_count)
                        VALUES (:type, :name, :time, :id, :comp, :pub, :rating, :rating_c) RETURNING recipe_id
                        """), {"type": temp_type, "name": temp_name, "id": user_id, "time": temp_time, "comp": temp_comp, "pub": True, "rating": rate, "rating_c": r_count}).fetchone()[0]
                
                count_i = int(random.randint(1, 10))
                ingredients = ["egg", "peanut butter", "flour", "sugar", "chocolate", "honey", "olive oil", 
                               "almonds", "rice", "milk", "pecans", "carrots", "pumpkin", "cinnamon", "ginger",
                               "caramel", "quinoa", "butter", "cream cheese", "almond milk", "brown sugar", "bananas",
                               "mango", "pineapple", "cauliflower", "avocado", "chickpeas", "nutmeg", "basil",
                               "tofu", "ricotta", "goat cheese", "matcha powder", "marshmallows", "soy sauce", "cherries"]
                measurment = ["cup", "oz", "tbs", "tsp", "half cup", "quarter cup", "half tbs", "g"]
                for i in range(count_i):
                    mod = random.randint(0, len(ingredients) - 1)
                    temp_ing = ingredients[mod]
                    mod = random.randint(0, len(measurment) - 1)
                    temp_meas = measurment[mod]
                    mod = random.randint(0, 5)

                    connection.execute(sqlalchemy.text("""
                                INSERT INTO ingredients (recipe_id, name, measurement_type, amount) 
                                VALUES (:id, :name, :type, :amount)
                                """), {"id": recipe_id, "name": temp_ing, "type": temp_meas, "amount": mod})
                    
                rec_tags = ["vegetarian", "dairy free", "gluten free", "vegan", "pescatarian", "keto", "high protein",
                             "easy", "quick", "no cook", "budget friendly", "meal prep", "healthy", "gourmet"]
                count_t = int(random.randint(0, 3))
                for t in range(count_t):
                    mod = random.randint(0, len(rec_tags) - 1)
                    temp_tag = rec_tags[mod]
                    connection.execute(sqlalchemy.text("""
                                INSERT INTO recipe_tags (recipe_id, tag) 
                                VALUES (:id, :tag)
                                """), {"id": recipe_id, "tag": temp_tag})
            
            count = random.randint(0, 5)
            for comment in range(count):
                recipe_id = connection.execute(sqlalchemy.text("SELECT recipe_id FROM recipes ORDER BY RANDOM() LIMIT 1")).fetchone().recipe_id
                temp_comment = ''.join(random.choices(string.ascii_letters,k=int(random.randint(10, 100))))

                connection.execute(sqlalchemy.text("INSERT INTO comments (user_id, recipe_id, comment) VALUES (:u_id, :r_id, :comment)"),
                                   {"r_id": user_id, "u_id": user_id, "comment": temp_comment})
                
            count = random.randint(0, 5)
            for fav in range(count):
                recipe_id = connection.execute(sqlalchemy.text("SELECT recipe_id FROM recipes ORDER BY RANDOM() LIMIT 1")).fetchone().recipe_id

                connection.execute(sqlalchemy.text("INSERT INTO favorites (user_id, recipe_id) VALUES (:u_id, :r_id)"),
                                   {"r_id": user_id, "u_id": user_id})

                




