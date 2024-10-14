**1. User Signup (POST)**  
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
   &nbsp;&nbsp;&nbsp;&nbsp;"email": "string",  
   &nbsp;&nbsp;&nbsp;&nbsp;"password": "string" 
   }    
   Response:  
  {  
   &nbsp;&nbsp;&nbsp;&nbsp;"user_id": "string" /* Returns a unique user_id */  
   }
     
**2. Login (POST)**  
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
   &nbsp;&nbsp;&nbsp;&nbsp;"password": "string",  
   }    
   Response:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"success": boolean  
   }  
**3. Recipe Posting (POST)**  
   Add Recipe to personal or social blog  
   Request:  
   {  
   &nbsp;&nbsp;&nbsp;&nbsp;"title": "string",  
   &nbsp;&nbsp;&nbsp;&nbsp;"ingredients": [{ingredient_type: "string", "measurement_type": "string", “quantity”: "int"}],  
   &nbsp;&nbsp;&nbsp;&nbsp;"time": "int",  
   &nbsp;&nbsp;&nbsp;&nbsp;"author_id": "int",  
   &nbsp;&nbsp;&nbsp;&nbsp;"is_public": "boolean"  
   }    
   Response:
   {
   &nbsp;&nbsp;&nbsp;&nbsp;"success": "boolean"
   }  
**4. Explore Recipes**  
   Filter for recipes based on certain preferences
   Request:  
   {
   &nbsp;&nbsp;&nbsp;&nbsp;“recipe_type”: “string”,  
   &nbsp;&nbsp;&nbsp;&nbsp;“preferences”: “string”,  
   &nbsp;&nbsp;&nbsp;&nbsp;“dietary_restrictions”: string”,  
   }    
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



        
