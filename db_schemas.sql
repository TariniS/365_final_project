-- DATABASE SCHEMAS


-- create user_table
CREATE TABLE users (
  user_id INT PRIMARY KEY,
  firstname VARCHAR(255),
  lastname VARCHAR(255));
  
-- create recipe_table
CREATE TABLE recipes (
  recipe_id INT PRIMARY KEY,
  recipe_name VARCHAR(255),
  user_id INT, -- Add the user_id column
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  total_time VARCHAR(255),
  servings INT,
  spicelevel INT,
  cookinglevel INT);

-- create ingredients_table
CREATE TABLE ingredients (
  ingredient_id INT PRIMARY KEY,
  recipe_id INT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
  ingredient_name VARCHAR(255),
  core_ingredient VARCHAR(255),
  quantity INT,
  measurement VARCHAR(255));

-- create instructions_table
CREATE TABLE instructions (
  instruction_id INT PRIMARY KEY,
  recipe_id INT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
  step_order INT,
  step_name VARCHAR(255));

-- create recipe_rating
CREATE TABLE ratings (
  rating_id INT PRIMARY KEY,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  recipe_id INT,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
  recipe_rating INT,
  recipe_comment VARCHAR(255),
  date DATE DEFAULT CURRENT_DATE);
