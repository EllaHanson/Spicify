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
   ```json
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
   &nbsp;&nbsp;&nbsp;&nbsp;"password": "string",  
   }
   ```
   Response:  
   ```json
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"success": boolean  
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
   ```json
   Request:  
   {
   “recipe_type”: “string”,  
   “preferences”: “string”,  
   “dietary_restrictions”: string”,  
   }
   ```
**5. Favorite Recipes**  
   Save a recipe for later in the favorites tab  
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;“recipe_id”: “string”,  
   }    
   Response:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;“success”: boolean  
   }
**6. Search User (GET)**  
   Search for specific username  
   Request:  
   {  
    &nbsp;&nbsp;&nbsp;&nbsp;“username”: string  
    &nbsp;&nbsp;&nbsp;&nbsp;“tag”: ["prefrence": "string"]  
   }    
   Response:  
   {  
    &nbsp;&nbsp;&nbsp;&nbsp;“users_result”: ["usernames": "int"]  
   }
**7. Edit Profile**  
   Change username, tags, about me, etc  
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;“username”: “string”,  
   &nbsp;&nbsp;&nbsp;&nbsp;“chef_level”: “string”,  
   &nbsp;&nbsp;&nbsp;&nbsp;“about_me”: “string”  
   }    
   Response:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"success": "boolean"  
   }  
**8. Logout**  
   Response:  
   {  
    &nbsp;&nbsp;&nbsp;&nbsp;"success": "boolean"  
   }  



        
