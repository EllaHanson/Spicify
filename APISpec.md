**1. User Access**  

**1.1 User Signup - /signup/ (POST)**  
   Request:  
   ```json
   {  
   "username": "string",  
   "email": "string",  
   "password": "string" 
   }
   ```
   Response:  
   ```json
   {  
   "user_id": "string" /* Returns a unique user_id */  
   }
   ```     
**1.2 Login - /login/ (POST)**  
   Request:  
   ```json
   {  
   "username": "string",  
   "password": "string"
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"
   }
   ```
**2. User Pages**  

**2.1 Get Favorites /blog/{user_id}/favorites/ (GET)**  
   Provide list of the user's favorited recipes.
   Request:
   ```json
   {
   "user_id": "int"
   }
   ```
   Response:  
   ```json
   {
   "user_favs": [{"recipe_id": "int"}]
   }
   ```
**2.2 Post a Recipe - blog/{user_id}/post-recipe/ (POST)**  
   Add Recipe to personal or social blog  
   Request:  
   ```json
   {
   "title": "string", 
   "ingredients": [{"ingredient_type": "string", "measurement_type": "string", “quantity”: "int"}],
   "method": "string",
   "time": "int",  
   "author_id": "int",  
   "is_public": "boolean" 
   }
   ```
   Response:
   ```json
   {
   "recipe_id": "string"
   }
   ```
**2.3 Edit Profile - /blog/{user_id}/edit-profile/ (PUT)**  
   Change username, chef level, or about me
   Request:  
   ```json
   {  
   "username": "string",  
   "chef_level": "string",  
   "about_me": "string"  
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"  
   }
   ```
**2.4 Logout - /blog/{user_id}/log-out (POST)**  
   Request:  
   ```json
   {  
   "user_id": "string",  
   "logged_in": "string" /* Should be set to false */
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"  
   }
   ```
**3. Explore Recipes**  

**3.1 Filter Recipes /explore/filter/ (GET)**  
   Filter for recipes based on certain preferences  
   Request:
   ```json
   {
   "recipe_type": "string",  
   "ingredients": [{"ingredient_type": "string", "measurement_type": "string", “quantity”: "int"}],  
   "dietary_restrictions": [{"dietary_restriction": "string"}]
   "max_time": "int",
   "chef_level": "string"
   }
   ```
   Response:  
   ```json
   {  
   "recipes_result": [{"recipe_id": "int"}]
   }
   ```
**3.2 Add a Recipe to Favorites /explore/{recipe-id}/favorites/ (POST)**  
   Save a recipe for later in the favorites tab  
   Request:  
   ```json
   {  
   "recipe_id": "string"
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"
   }
   ```
**3.3 Comment on Recipes /explore/{recipe-id}/comments/ (POST)**  
   Comment on a recipe in the recipe feed 
   Request:  
   ```json
   {  
    "recipe_id": "string",
    "message": "string" 
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean" 
   }
   ```

**3.4 Rate a Recipe /explore/{recipe-id}/rate/ (POST)**  
   Rate a recipe in the recipe feed 
   Request:  
   ```json
   {  
    "recipe_id": "string"
    "rating": "int" 
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"
   }
   ```





        
