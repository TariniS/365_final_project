-- NOTE FOR PROFESSOR:
-- initally, we made all the tables using sql CREATE function. To get the ground running, we inserted one line of sample data
-- into each of the tables (which is shown above) and implented out get and post requests accordingly!

-- create ingredients_table
INSERT INTO ingredients (recipe_id, ingredient_id, ingredient_name, core_ingredient, quantity, measurement)
VALUES (0, 0, 'cheddar cheese', 'cheese', 2, 'slices'),
(0, 1, 'sourdough bread', 'bread', 2, 'slices'),
(0, 2, 'unsalted butter', 'butter', 1, 'tablespoon'),
(0, 3, 'oregano', 'oregano', 1, 'pinch'),
(1, 4, 'spaghetti', 'pasta', 2, 'cups'),
(1, 5, 'lemon pepper seasoning', 'pepper', 2, 'tablespoons'),
(1, 6, 'black pepper seasoning', 'pepper', 2, 'tablespoons'),
(1, 7, 'unsalted butter', 'butter', 1.5, 'tablespoons'),
(1, 8, 'chili powder', 'paprika', 0.5, 'tablespoon'),
(1, 9, 'minced garlic', 'garlic', 2, 'tablespoons'),
(1, 10, 'shredded mozarella cheese', 'cheese', 0.5, 'cup'),
(1, 11, 'water', 'water', 8, 'cups'),
(1, 12, 'salt', 'salt', 1, 'pinch')


-- create instructions_table
INSERT INTO instructions (instruction_id, recipe_id, step_order, step_name)
VALUES (0, 0, 0, 'Preheat a non-stick skillet or griddle over medium heat.'),
(1, 0, 1, 'Butter one side of two slices of sourdough bread and place one slice, buttered-side down, in the skillet.'),
(2, 0, 2, 'Place 1-2 slices of cheddar cheese on top of the bread in the skillet, and then top with the second slice of bread, buttered-side up.'),
(3, 0, 3, 'Sprinkle 1 pinch of oregano on top of the bread.'),
(4, 0, 4, 'Cook until the bread is golden brown and the cheese is melted, about 2-3 minutes per side.'),
(5, 0, 5, 'Remove from the skillet and let cool for a minute before slicing and serving.')

-- create recipe_table
INSERT INTO recipe(recipe_id, recipe_name, user_id, total_time, servings, spicelevel, cookinglevel, recipe_description)
VALUES(0, 'Grilled Cheese', 0, '10 mins', 1, 0, 1, 'quick vegetarian snack or meal')


-- create user_table
INSERT INTO users (user_id, user_name)
VALUES (1, 'mary jane'),
(2, 'susan boykin'),
(3, 'andrew garfield'),
(4, 'tom holland'),
(5, 'zendaya')

-- create recipe_rating
INSERT INTO recipe_rating(rating_id, user_id, recipe_id, recipe_rating, recipe_comment, date)
VALUES (3, 4, 1, 8, 'wow, best pasta ever!', current_date),
(4, 2, 1, 5, 'Easy to make for college students', current_date)
