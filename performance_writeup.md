# Fake Data Modeling

https://github.com/EllaHanson/Spicify/blob/main/src/api/populate.py

## Final Rows

Comments: 26,006
It makes sense that users would be able to make multiple comments.

Favorites: 25,979
It makes sense that users would favorite great recipes, and some recipes would not be favorited at all because they may be nasty.

Ingredients: 288,527
It should scale this way because recipes use all sorts of ingredients. It takes different ingredients to make a pumpkin pie compared to a stuffed turkey.

Profile_info: 1,072,617
It should match the number of users, which it does.

Recipe_tags: 78,682
It scales this way because a recipe can have multiple tags. For example, eggs can have the tags of healthy and high protein.

Recipes: 52,394
It makes sense that users would make multiple recipes for different purposes instead of just one. But not every user would make one and simply follow an already made recipe.

User_tags: 61,833
A user should be able to pick multiple tags. For example, a user may be vegan and wanting high protein. But not every user will care to pick one.

Users: 1,072,617
This many users should use our service because it is the best out there. It should also match the number of profile infos, which it does.

Total rows: 2,678,655
A bit more than a million rows.

# Performance results of hitting endpoints

**Average execution time:**

/recipe/delete/recipe - 413.54 ms **Slowest**

/recipe/get/recipe - 374.84 ms **2nd Slowest**

/favorites/explore/favorites - 287.58 ms **3rd Slowest**

/profiles/delete/profile - 182.64 ms 

/profiles/patch/profile - 176.09 ms 

/profiles/post/user - 171.78 ms 

/recipe/post/recipe - 170.98 ms

/post/comments - 144.23 ms

/favorites/blog/favorites - 125.51 ms

/profiles/put/loggin - 121.31 ms

/profiles/put/loggout - 111.31 ms

/rating/post/rating - 96.25 ms

# Performance tuning

## /recipe/delete/recipe

### EXPLAIN SELECT COUNT(*) FROM recipes WHERE recipe_id = :id
```
('Aggregate  (cost=1.41..1.42 rows=1 width=8)',)
('  ->  Index Only Scan using recipes_pkey on recipes  (cost=0.29..1.41 rows=1 width=0)',)
('        Index Cond: (recipe_id = 72434)',)
```
This query cannot be made more efficient since recipe_id is the primary key. There is no need for indexing here.

### EXPLAIN DELETE FROM recipes WHERE recipe_id = :id
```
('Delete on recipes  (cost=0.29..2.51 rows=0 width=0)',)
('  ->  Index Scan using recipes_pkey on recipes  (cost=0.29..2.51 rows=1 width=6)',)
('        Index Cond: (recipe_id = 72434)',)
```
This query is analogous to the previous one for the same reason. No need for indexing.

### EXPLAIN DELETE FROM ingredients WHERE recipe_id = :id
```
('Delete on ingredients  (cost=0.00..6027.54 rows=0 width=0)',)
('  ->  Seq Scan on ingredients  (cost=0.00..6027.54 rows=7 width=6)',)
('        Filter: (recipe_id = 72434)',)
```
The cost is unbelievably high. It seems that it is scanning the entire ingredients table. An index should be placed on recipe_id.
CREATE INDEX indx_ingr ON ingredients (recipe_id)
```
('Delete on ingredients  (cost=0.42..2.75 rows=0 width=0)',)
('  ->  Index Scan using indx_ingr on ingredients  (cost=0.42..2.75 rows=7 width=6)',)
('        Index Cond: (recipe_id = 72434)',)
```
This query has had the performance improvement I expected.

### EXPLAIN DELETE FROM recipe_tags WHERE recipe_id = :id
```
('Delete on recipe_tags  (cost=0.00..1553.00 rows=0 width=0)',)
('  ->  Seq Scan on recipe_tags  (cost=0.00..1553.00 rows=2 width=6)',)
('        Filter: (recipe_id = 72434)',)
```
The cost is high as well here for similar reasons. An index should be placed on recipe_id.
CREATE INDEX indx_r_tags ON recipe_tags (recipe_id)
```
('Delete on recipe_tags  (cost=0.29..2.53 rows=0 width=0)',)
('  ->  Index Scan using indx_r_tags on recipe_tags  (cost=0.29..2.53 rows=2 width=6)',)
('        Index Cond: (recipe_id = 72434)',)
```
This query has also improved in the manner that I expected.

## /recipe/get/recipe

### EXPLAIN SELECT DISTINCT recipe_id FROM recipe_tags WHERE tag IN (" + tags_param + ") GROUP BY recipe_id HAVING COUNT(DISTINCT tag) = :tag_count LIMIT 15
```
('Limit  (cost=1868.96..1929.99 rows=15 width=4)',)
('  ->  Unique  (cost=1868.96..1978.82 rows=27 width=4)',)
('        ->  GroupAggregate  (cost=1868.96..1978.75 rows=27 width=4)',)
('              Group Key: recipe_id',)
('              Filter: (count(DISTINCT tag) = 1)',)
('              ->  Sort  (cost=1868.96..1883.06 rows=5641 width=13)',)
('                    Sort Key: recipe_id',)
('                    ->  Seq Scan on recipe_tags  (cost=0.00..1517.47 rows=5641 width=13)',)
("                          Filter: (tag = 'healthy'::text)",)
```
This query is inefficient. There should be an index place on recipe_id and tag.
```
('Limit  (cost=0.42..630.46 rows=15 width=4)',)
('  ->  Unique  (cost=0.42..1134.49 rows=27 width=4)',)
('        ->  GroupAggregate  (cost=0.42..1134.42 rows=27 width=4)',)
('              Group Key: recipe_id',)
('              Filter: (count(DISTINCT tag) = 1)',)
('              ->  Index Only Scan using indx_r_tag on recipe_tags  (cost=0.42..1038.73 rows=5641 width=13)',)
```
This query is relatively more efficient than previously.

### EXPLAIN SELECT DISTINCT recipe_id FROM ingredients WHERE name IN (" + ing_param + ") GROUP BY recipe_id HAVING COUNT(DISTINCT ingredient_id) = :ing_count LIMIT 15
```
('Limit  (cost=0.42..3208.41 rows=15 width=4)',)
('  ->  Unique  (cost=0.42..7913.45 rows=37 width=4)',)
('        ->  GroupAggregate  (cost=0.42..7913.36 rows=37 width=4)',)
('              Group Key: recipe_id',)
('              Filter: (count(DISTINCT ingredient_id) = 1)',)
('              ->  Index Scan using indx_ingr on ingredients  (cost=0.42..7782.33 rows=7915 width=12)',)
("                    Filter: (name = 'egg'::text)",)
[('Limit  (cost=0.42..3208.41 rows=15 width=4)',), ('  ->  Unique  (cost=0.42..7913.45 rows=37 width=4)',), ('
->  GroupAggregate  (cost=0.42..7913.36 rows=37 width=4)',), ('Group Key: recipe_id',), ('Filter: (count(DISTINCT ingredient_id) = 1)',),
('->  Index Scan using indx_ingr on ingredients  (cost=0.42..7782.33 rows=7915 width=12)',), ("Filter: (name = 'egg'::text)",)]
```
This query is extremely inefficient. There should be indexes on name and ingredient_id

### EXPLAIN SELECT DISTINCT recipe_id FROM ingredients WHERE name IN (" + ing_param + ") GROUP BY recipe_id HAVING COUNT(DISTINCT ingredient_id) = :ing_count LIMIT 15
```
('Limit  (cost=0.42..1721.48 rows=15 width=4)',)
('  ->  Unique  (cost=0.42..4245.69 rows=37 width=4)',)
('        ->  GroupAggregate  (cost=0.42..4245.59 rows=37 width=4)',)
('              Group Key: recipe_id',)
('              Filter: (count(DISTINCT ingredient_id) = 1)',)
('              ->  Index Only Scan using indx_ingr_n_and_ingr_id on ingredients  (cost=0.42..4114.57 rows=7915 width=12)',)
("                    Index Cond: (name = 'egg'::text)",)
```
Compared to what it once was, it's pretty good.

### EXPLAIN SELECT recipe_id FROM recipes WHERE type = :recipe_type and time_needed < :time and complexity = :level LIMIT 15
```
('Limit  (cost=0.00..8.84 rows=15 width=8)',)
('  ->  Seq Scan on recipes  (cost=0.00..2001.61 rows=3398 width=8)',)
("        Filter: ((time_needed < 200) AND (type = 'lunch'::text) AND (complexity = 'chef'::text))",)
```
It is costing a lot to scan recipes. It should be indexing on time_needed, type, and complexity.

CREATE INDEX recipe_filter ON recipes (type, complexity, time_needed)
```
('Limit  (cost=0.29..5.76 rows=15 width=8)',)
('  ->  Index Scan using recipe_filter on recipes  (cost=0.29..1184.19 rows=3244 width=8)',)
("        Index Cond: ((type = 'lunch'::text) AND (complexity = 'chef'::text) AND (time_needed < 200))",)
```
It is costing a lot less now.

## /favorites/explore/favorites

### EXPLAIN SELECT COUNT(*) FROM users WHERE user_id = :id

```
('Aggregate  (cost=1.55..1.56 rows=1 width=8)',)
('  ->  Index Only Scan using users_pkey on users  (cost=0.43..1.55 rows=1 width=0)',)
("        Index Cond: (user_id = '69990'::bigint)",)
```
This query is already really efficient thanks to the implementation of its primary key: user_id

### EXPLAIN SELECT COUNT(*) FROM recipes WHERE recipe_id = :id

```
('Aggregate  (cost=2.51..2.52 rows=1 width=8)',)
('  ->  Index Only Scan using recipes_pkey on recipes  (cost=0.29..2.51 rows=1 width=0)',)
("        Index Cond: (recipe_id = '17999'::bigint)",)
```
This query is efficient for similar reasons as the previous one.

### 

```
('Insert on favorites  (cost=0.00..0.01 rows=0 width=0)',)
('  ->  Result  (cost=0.00..0.01 rows=1 width=16)',)
```
This query also performs exceptionally well.

Not sure why this endpoint is relatively slow.
