import random
import string
import datetime
import database as db
from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#############################################################################
# Bulk_Insert Script
# BEFORE RUNNING MAKE SURE YOU ARE CONNECTED TO YOUR LOCAL DB
# AND THAT THE LOCAL DB IS COMPLETELY EMPTY
# Run using: python ./src/bulk_insert.py
#############################################################################

# Generate random recipe names
def generate_recipe_name():
    words = ["Apple", "Banana", "Chocolate", "Egg", "Fish", "Ginger", "Honey", "Ice Cream", "Jam", "Cream"]
    style = ["Foster", "Bread", "Pie", "Croissant", "Tart", "Donut", "Pastry", "Sandwhich", "Toast", "Soup"]

    return random.choice(words) + random.choice(style)

# Generate random total times
def generate_total_time():
    return random.randint(10, 120)

# Generate random servings
def generate_servings():
    return random.randint(1, 10)

# Generate random spice levels
def generate_spice_level():
    return random.randint(1, 5)

# Generate random cooking levels
def generate_cooking_level():
    return random.randint(1, 3)

# Generate random recipe types
def generate_recipe_type():
    types = ["Food", "Drink", "Dessert"]
    return random.choice(types)

# Generate random step text
def generate_step_name():
    step_names = ["Preheat the oven", "Mix the ingredients", "Chop the vegetables", "Sauté the onions", "Bake for 30 minutes"]
    return random.choice(step_names)

# Generate random core ingredient names
def generate_core_ingredient():
    names = ["Salt", "Sugar", "Flour", "Butter", "Milk", "Eggs", "Tomatoes", "Onions", "Garlic", "Pepper"]
    return random.choice(names)

# Generate random flavor + ingredient combinations
def generate_ingredient_name(num):
    flavor = ["Caramel", "Peanut", "Sourdough", "Lemon", "Tomato", "Sugar", "Ginger"]
    ingredients = ["Salt", "Sugar", "Flour", "Butter", "Milk", "Eggs", "Tomatoes", "Onions", "Garlic", "Pepper"]
    return random.choice(flavor) + " " + random.choice(ingredients) + " " + str(num)

# Generate random measurement
def generate_measurement():
    measurements = ["g", "kg", "ml", "l", "tsp", "tbsp"]
    return random.choice(measurements)

# Generate random recipe comments
def generate_recipe_comment():
    comments = ["Great recipe!", "Delicious!", "Easy to make", "Tasty!", "Highly recommended"]
    return random.choice(comments)

# Generate random timestamps
def generate_timestamp():
    # Generate a date within the past year
    start_date = datetime.datetime.now().date()
    random_date =  start_date + datetime.timedelta(random.randint(-365, 365))
    return random_date

# Generate random tag for the dish
def generate_tag(num):
    tags = ["String", "nuts", "sweet", "chocolate", "baked", "coffee", "iced", "fish"]
    return random.choice(tags) + str(num)

# Generate random user first names
def generate_user_firstname():
    firstnames = ["John", "Jane", "Alice", "Bob", "David", "Emily", "Michael", "Olivia", "Sophia", "William"]
    return random.choice(firstnames)

# Generate random user last names
def generate_user_lastname():
    lastnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    return random.choice(lastnames)

# Generate random usernames
def generate_username():
    return generate_user_firstname().lower() + str(random.randint(1, 1000))

# Generate random passwords
def generate_password(len):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=len))

# Generate 1 million recipes
def generate_recipe_entries():
    recipe_entries = []
    for i in range(0, 1000000):
        entry = {
            "recipe_id": i,
            "recipe_name": generate_recipe_name(),
            "user_id": 0,
            "total_time": generate_total_time(),
            "servings": generate_servings(),
            "spice_level": generate_spice_level(),
            "cooking_level": generate_cooking_level(),
            "recipe_type": generate_recipe_type()
        }
        recipe_entries.append(entry)
    return recipe_entries

# Generate 1 million instructions
def generate_instruction_entries():
    instruction_entries = []
    for i in range(0, 1000000):
        entry = {
            "instruction_id": i,
            "recipe_id": 0,
            "step_order": random.randint(1, 99),
            "step_name": generate_step_name()
        }
        instruction_entries.append(entry)
    return instruction_entries

# Generate 1 million ingredients
def generate_ingredient_entries():
    ingredient_entries = []
    for i in range(0, 1000000):
        entry = {
            "ingredient_id": i,
            "name": generate_ingredient_name(i),
            "core_ingredient": generate_core_ingredient()
        }
        ingredient_entries.append(entry)
    return ingredient_entries

# Generate 1 million recipe ingredients
def generate_recipe_ingredient_entries():
    r_i_entries = []
    for i in range(0, 1000000):
        entry = {
            "recipe_id": i,
            "ingredient_id": 0,
            "quantity": random.randint(1, 99),
            "measurement": generate_measurement()
        }
        r_i_entries.append(entry)
    return r_i_entries

# Generate 1 million recipe ratings
def generate_recipe_rating_entries():
    r_r_entries = []
    for i in range(0, 1000000):
        entry = {
            "rating_id": i,
            "recipe_id": 0,
            "user_id": 0,
            "recipe_rating": random.randint(0, 10),
            "recipe_comment": generate_recipe_comment(),
            "time_stamp": generate_timestamp()
        }
        r_r_entries.append(entry)
    return r_r_entries

# Generate 1 million tags
def generate_tag_entries():
    t_entries = []
    for i in range(0, 1000000):
        entry = {
            "tag_id": i,
            "tag": generate_tag(i)
        }
        t_entries.append(entry)
    return t_entries

# Generate 1 million recipe_tags
def generate_recipe_tag_entries(tag_entries):
    r_t_entries = []
    for i in range(0, 1000000):
        entry = {
            "tag_id": i,
            "recipe_id": random.randint(0, 999999),
            "tag": generate_tag(i)
        }
        r_t_entries.append(entry)
    return r_t_entries

# Generate 1 million users
def generate_user_entries():
    user_entries = []
    for i in range(0, 1000000):
        entry = {
            "user_id": i,
            "firstname": generate_user_firstname(),
            "lastname": generate_user_lastname(),
            "username": generate_username(),
            "password": generate_password(random.randint(8,16))
        }
        user_entries.append(entry)
    return user_entries

# Create a session
Session = sessionmaker(bind=db.engine)
session = Session()

# Generate entries
recipe_entries = generate_recipe_entries()
instruction_entries = generate_instruction_entries()
ingredient_entries = generate_ingredient_entries()
recipe_ingredient_entries = generate_recipe_ingredient_entries()
recipe_rating_entries = generate_recipe_rating_entries()
tag_entries = generate_tag_entries()
recipe_tag_entries = generate_recipe_tag_entries(tag_entries)
user_entries = generate_user_entries()

Base = declarative_base()

# Define the Table Schemas
class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String)
    core_ingredient = Column(String)

class Instruction(Base):
    __tablename__ = 'instructions'
    instruction_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
    step_order = Column(Integer)
    step_name = Column(String)

class Recipe_Ingredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer)
    quantity = Column(Float)
    measurement = Column(String)

class Recipe_Rating(Base):
    __tablename__ = 'recipe_ratings'
    rating_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
    user_id = Column(Integer)
    recipe_rating = Column(Integer)
    recipe_comment = Column(String)
    time_stamp = Column(Date)

class Recipe_Tag(Base):
    __tablename__ = 'recipe_tags'
    tag_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
    tag = Column(Text)

class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True)
    recipe_name = Column(String)
    user_id = Column(Integer)
    total_time = Column(Integer)
    servings = Column(Integer)
    spice_level = Column(Integer)
    cooking_level = Column(Integer)
    recipe_type = Column(String)

class Tag(Base):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True)
    tag = Column(Text)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String)
    password = Column(String)

# Perform bulk insert
session.bulk_insert_mappings(User, user_entries)
print(".")

session.bulk_insert_mappings(Recipe, recipe_entries)
print(".")

session.bulk_insert_mappings(Instruction, instruction_entries)
print(".")

session.bulk_insert_mappings(Ingredient, ingredient_entries)
print(".")

session.bulk_insert_mappings(Recipe_Ingredient, recipe_ingredient_entries)
print(".")

session.bulk_insert_mappings(Recipe_Rating, recipe_rating_entries)
print(".")

session.bulk_insert_mappings(Tag, tag_entries)
print(".")

session.bulk_insert_mappings(Recipe_Tag, recipe_tag_entries)

print(". committing...")

# Close the session
session.close()

print("Bulk insert completed successfully.")
