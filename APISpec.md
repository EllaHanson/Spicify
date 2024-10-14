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
**1.3 Logout - /blog/{user-id}/ (POST)**  
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
**2. Post a Recipe - /postrecipe/ (POST)**  
   Add Recipe to personal or social blog  
   Request:  
   ```json
   {
   "title": "string", 
   "ingredients": [{"ingredient_type": "string", "measurement_type": "string", “quantity”: "int"}],  
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
**3. Explore Recipes**  
**3.1 Filter Recipes /explore/ (POST)**  
   Filter for recipes based on certain preferences  
   Request:
   ```json
   {
   "recipe_type": "string",  
   "ingredients": [{"ingredient_type": "string", "measurement_type": "string", “quantity”: "int"}],  
   "dietary_restrictions": [{"dietary_restriction": "string"}]
   }
   ```
   Response:  
   ```json
   {  
   "recipes_result": [{"recipe_id": "int"}]
   }
   ```
**3.2 Favorite Recipes /explore/favorites/ (POST)**  
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
**6. Get Favorites /blog/favorites/ (GET)**  
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

**7. Search User (POST)**  
   Search for specific username  
   Request:  
   ```json
   {  
    "username": "string"  
    "tag": ["prefrence": "string"]  
   }
   ```
   Response:  
   ```json
   {  
   "users_result": ["usernames": "int"]  
   }
   ```
**8. Edit Profile (PUT)**  
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




        
