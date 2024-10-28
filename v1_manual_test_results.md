# Example workflow
**Teresa is a new user. She is a home cook mom who visits our recipe site looking for fast and easy recipe ideas for her family of 5...**
- Teresa first calls POST /signup to create a new account. She passes in her email, username, and password. A unique user_id 1001 is created.
- Teresa now logs in to her account. She calls POST /login and passes in her username and password, the logged in state returns "true", logging Teresa in successfully.
- Teresa navigates to her profile to update it. She calls PUT /blog/{1001}/edit-profile and adds an about me section and changes her chef level to "home cook".


# Testing results  
##/recipe/post/user  
1.  
```
curl -X 'POST' \  
  'http://127.0.0.1:8000/recipe/post/user' \  
  -H 'accept: application/json' \  
  -H 'access_token: a' \  
  -H 'Content-Type: application/json' \  
  -d '{  
  "name": "Teresa",  
  "email": "TeresaIsCool@gmail.com",  
  "password": "lol_itz_teresa"  
}'
```
  
2.  
<ins>code</ins>: 200  
<ins>Response Body</ins>:
```json
{
  "user_id": 7
}
```
<ins>Response Header:</ins>  
```
 access-control-allow-credentials: true   
 content-length: 13  
 content-type: application/json  
 date: Mon,28 Oct 2024 20:02:35 GMT  
 server: uvicorn  
```
  
##/recipe/loggin  
1.  
```
curl -X 'POST' \  
  'http://127.0.0.1:8000/recipe/loggin?user_id=7' \  
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
 date: Mon,28 Oct 2024 20:05:10 GMT  
 server: uvicorn  
```
  
##/recipe/profile  
1.  
```
curl -X 'POST' \  
  'http://127.0.0.1:8000/recipe/profile?id=7&level=home%20cook&about_me=Looking%20for%20pies%20for%20Thanksgiving%21%21' \   
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
 date: Mon,28 Oct 2024 20:15:33 GMT  
 server: uvicorn  
```
  
