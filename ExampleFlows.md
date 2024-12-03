**Teresa is a new user. She is a home cook mom who visits our recipe site looking for fast and easy recipe ideas for her family of 5...**
- Teresa first calls POST /signup to create a new account. She passes in her email, username, and password. A unique user_id 1001 is created.
- Teresa now logs in to her account. She calls POST /login and passes in her username and password, the logged in state returns "true", logging Teresa in successfully.
- Teresa navigates to her profile to update it. She calls PUT /blog/{1001}/edit-profile and adds an about me section and changes her chef level to "home cook".

**Teresa is now a returning user. She wants to explore new recipes to add to her collection...**
- Teresa navigates to the Explore Recipes tab to look for new recipes. She calls POST /explore/filter and passes in "dinner" for recipe type, "keto" for dietary restrictions, 30 minutes for max time, and home cook for complexity level.
- Teresa scrolls through the filtered feed of recipes. She finds a recipe she loves and wants to add it to her favorites. She clicks on the recipe of recipe ID 2001 and calls POST /explore/{2001}/favorites, which adds it to her list of favorites for later.
- She tries out the recipe for dinner and loved it. Now, she wants to comment and rate the recipe. She calls POST /explore/{2001}/comment and passes in her comment "This shrimp scampi was fast, easy, and delicious! Great crowd pleaser." She also calls POST /explore/{2001}/rate and passes a "5" for rating, giving it a 5-star rating. 

**Teresa now wants to post a new recipe that she had created in her spare time to share with others...**
- Teresa navigates to her recipe blog and calls POST blog/{1001}/post-recipe to post a new recipe. She passes in "Pesto Chicken and Veggies" for title, "chicken", "green beans", "olive oil", and "pesto" for ingredients, and her recipe instructions for method. After the call, the recipe is posted and a new recipe ID 2002 is created for this recipe.
- Now, Teresa wants to log out to protect her data. She calls POST /blog/{1001}/log-out and successfully logs out of her account.


