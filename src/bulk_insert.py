import random
import database as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Generate random recipe names
def generate_recipe_name():
    words = ["Apple", "Banana", "Chocolate", "Delicious", "Egg", "Fish", "Ginger", "Honey", "Ice Cream", "Jam"]
    return random.choice(words) + " Recipe"

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
    types = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"]
    return random.choice(types)

# Generate 1 million entries
def generate_entries():
    entries = []
    for i in range(1, 1000001):
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
        entries.append(entry)
    return entries

# Create a session
Session = sessionmaker(bind=db.engine)
session = Session()

# Generate entries
entries = generate_entries()

Base = declarative_base()

# Define the Recipe model
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

# Perform bulk insert
session.bulk_insert_mappings(Recipe, entries)

# Commit the transaction
session.commit()

# Close the session
session.close()

print("Bulk insert completed successfully.")
