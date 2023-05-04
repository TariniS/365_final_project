import sqlalchemy
from sqlalchemy import func
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from typing import List

router = APIRouter()
@router.get("/recipes/{id}", tags=["recipes"])
def get_recipe(id: str):
    """
    GET /recipes/{id}:
  - This endpoint allows a user to view a recipe and see its rating and comments from other users for that specific recipe.
  - Parameters:
    - id: string (required)
  - Returns:
     [{recipe_name: name, user_id : id, total_time: int, servings: int, spice_level: int, cooking_level: int, recipe_description: String,
            ingredients: [{ ingredient_id : id, ingredient_name : name, quantity: quantity, measurements: units},
                         { ingredient_id : id, ingredient_name : name, quantity: quantity, measurements: units},
                         { ingredient_id : id, ingredient_name : name, quantity: quantity, measurements: units},
                         { ingredient_id : id, ingredient_name : name, quantity: quantity, measurements: units}],
            instructions: [{ instruction_id : id, step_order : step, step_name : name},
                           { instruction_id : id, step_order : step, step_name : name},
                           { instruction_id : id, step_order : step, step_name : name}],
            ratings: [{ rating_id : id, user_id : id, rating: int, comment: text },
                      {rating_id : id, user_id : id, rating: int, comment: text }]]
    """
    return id



@router.get("/recipes/", tags=["recipes"])
def get_recipes_by_ingredients(ingredient_list: str):
    json = None
    ingredient_list = ingredient_list.split(",")
    """
    - This endpoint allows a user to search for recipes based on ingredients they have available on hand and returns
    the recipes in order of highest ingredient match
  - Parameters:
    - ingredients: list of strings (required)
  - Returns List of Recipes: Top 5 based on highest ingredient match

        [{recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id}]
    """

    query = """ SELECT ingredients.recipe_id, recipe.recipe_name, COUNT(*) AS frequency
                from ingredients
                JOIN recipe ON ingredients.recipe_id = recipe.recipe_id
                WHERE ingredients.core_ingredient = ANY(:ingredient_list)
                GROUP BY ingredients.recipe_id, recipe.recipe_name 
                ORDER BY frequency DESC"""

    result = db.conn.execute(sqlalchemy.text(query), {'ingredient_list': ingredient_list})
    for row in result:
        json = {
            "recipe_name": row[1],
            "recipe_id": row[0]

        }

    return json


class recipe_sort_options(str, Enum):
    rating = "rating"
    spiceLevel = "spice_level"
    cookingLevel = "cooking_level"
    servings = "servings"


# Add get parameters
@router.get("/recipes/", tags=["movies"])
def list_recipes(
    tag: str = "",
    sort: recipe_sort_options = recipe_sort_options.rating):

    """
    currently only supports filtering by one tag?
    This endpoint allows a user to search for recipes based on tags, and sort/filter based on rating.
  - Parameters:
    - id: string (required)
    - tag: string (optional)
    - sort: sort.ratings (optional)

        [{recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id},
         {recipe_name : name, recipe_id : id}]

 - Returns a list of recipes  Top 5
"""

    return None




