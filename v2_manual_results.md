# Example workflows

## Teresa is now a returning user. She wants to explore new recipes to add to her collection...

- Teresa navigates to the Explore Recipes tab to look for new recipes. She calls POST /explore/filter and passes in "dinner" for recipe type, "keto" for dietary restrictions, 30 minutes for max time, and home cook for complexity level.
- Teresa scrolls through the filtered feed of recipes. She finds a recipe she loves and wants to add it to her favorites. She clicks on the recipe of recipe ID 2001 and calls POST /explore/{2001}/favorites, which adds it to her list of favorites for later.
- She tries out the recipe for dinner and loved it. Now, she wants to comment and rate the recipe. She calls POST /explore/{2001}/comment and passes in her comment "This shrimp scampi was fast, easy, and delicious! Great crowd pleaser." She also calls POST /explore/{2001}/rate and passes a "5" for rating, giving it a 5-star rating.

## Teresa now wants to post a new recipe that she had created in her spare time to share with others...

- Teresa navigates to her recipe blog and calls POST blog/{1001}/post-recipe to post a new recipe. She passes in "Pesto Chicken and Veggies" for title, "chicken", "green beans", "olive oil", and "pesto" for ingredients, and her recipe instructions for method. After the call, the recipe is posted and a new recipe ID 2002 is created for this recipe.
- Now, Teresa wants to log out to protect her data. She calls POST /blog/{1001}/log-out and successfully logs out of her account.

# Testing results  
## /recipe/post/recipe  
1.  
```
curl -X 'POST' \
  'http://127.0.0.1:8000/recipe/post/recipe?user_id=11' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "The Best Cheesecake Recipe",
  "type": "dessert",
  "time": 95,
  "complexity": "medium",
  "is_public": true,
  "ingredients": [
    {"name": "graham cracker crumbs","measurement_type": "half cup","measurement_amount": 3},
    {"name": "sugar","measurement_type": "cup","measurement_amount": 1},
    {"name": "brown sugar","measurement_type": "tablespoon","measurement_amount": 1},
    {"name": "butter","measurement_type": "tablespoon","measurement_amount": 7},
    {"name": "cream cheese","measurement_type": "oz","measurement_amount": 32},
    {"name": "sour cream","measurement_type": "third cup","measurement_amount": 2},
    {"name": "vanilla extract","measurement_type": "half teaspoon","measurement_amount": 3},
    {"name": "egg","measurement_type": "whole egg","measurement_amount": 4},
    {"name": "salt","measurement_type": "half teaspoon","measurement_amount": 1}
  ],
  "tags": [
    "luxurious"
  ]
}'
```
  
2.  
<ins>code</ins>: 200  
<ins>Response Body</ins>:
```json
{
  "OK"
}
```
<ins>Response Header:</ins>  
```
 access-control-allow-credentials: true 
 content-length: 4 
 content-type: application/json 
 date: Tue,05 Nov 2024 05:01:28 GMT 
 server: uvicorn 
```


## /recipe/get/filter  
1.  
```
curl -X 'POST' \
  'http://127.0.0.1:8000/recipe/get/filter?recipe_type=dessert&max_time=100' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "tags": [
  ],
  "ingredients": [
    "sugar", "egg"
  ]
}'
```
  
2.  
<ins>code</ins>: 200  
<ins>Response Body</ins>:
```json
{
  [5,6]
}
```
<ins>Response Header:</ins>  
```
 access-control-allow-credentials: true 
 content-length: 5 
 content-type: application/json 
 date: Tue,05 Nov 2024 05:06:48 GMT 
 server: uvicorn 
```

## /comment/post/comment  
1.  
```
curl -X 'POST' \
  'http://127.0.0.1:8000/comment/post/comment?user_id=12&recipe_id=6&comment=ehh' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''
```
  
2.  
<ins>code</ins>: 200  
<ins>Response Body</ins>:
```json
{
  "comment_id": 6
}
```
<ins>Response Header:</ins>  
```
 access-control-allow-credentials: true 
 content-length: 16 
 content-type: application/json 
 date: Tue,05 Nov 2024 05:10:47 GMT 
 server: uvicorn 
```
## /rating/post/rating
1. Curl
```
curl -X 'POST' \
  'http://127.0.0.1:8000/rating/post/rating?recipe_id=6&rating=5' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''
```
2. Response
_Response Body_
```
"OK"
```
_Response Header_
```
access-control-allow-credentials: true 
content-length: 4 
content-type: application/json 
date: Tue,05 Nov 2024 06:45:45 GMT 
server: uvicorn 
```

## Workflow: Teresa navigates to her profile to update it. She calls PUT /blog/{1001}/edit-profile and adds an about me section and changes her chef level to "home cook". 

## /update_profile/profile
1. 
```
curl -X 'POST' \
  'http://127.0.0.1:8000/profile/profile?id=7&level=home%20cook&about_me=yay%20i%20love%20cooking&username=TeresaLovesCooking&user_id=7' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''
```
2. 

<ins>Code</ins>: 200  
<ins>Response Body</ins>: 
```json
"OK"
```
 <ins>Response Header</ins>: 
```
 access-control-allow-credentials: true 
 content-length: 4 
 content-type: application/json 
 date: Tue,05 Nov 2024 06:20:14 GMT 
 server: uvicorn 
```
