**1. User Signup (POST)**  
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
     
**2. Login (POST)**  
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
**3. Recipe Posting (POST)**  
   Add Recipe to personal or social blog  
   Request:  
   ```json
   {  
   "title": "string",  
   "ingredients": [{ingredient_type: "string", "measurement_type": "string", “quantity”: "int"}],  
   "time": "int",  
   "author_id": "int",  
   "is_public": "boolean"  
   }
   ```
   Response:
   ```json
   {
   "success": "boolean"
   }
   ```
**4. Explore Recipes**  
   Filter for recipes based on certain preferences
   Request:
   ```json
   {
   “recipe_type”: “string”,  
   “preferences”: “string”,  
   “dietary_restrictions”: "string”
   }
   ```
**5. Favorite Recipes**  
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
**6. Search User (GET)**  
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
**7. Edit Profile**  
   Change username, tags, about me, etc  
   Request:  
   ```json
   {  
   “username”: “string”,  
   “chef_level”: “string”,  
   “about_me”: “string”  
   }
   ```
   Response:  
   ```json
   {  
   "success": "boolean"  
   }
   ```
**8. Logout**  
   Response:  
   ```json
   {  
   "success": "boolean"  
   }
   ```



        
