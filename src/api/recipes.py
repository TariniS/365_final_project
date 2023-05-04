import sqlalchemy
from sqlalchemy import func
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

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
def get_recipes_by_ingredients(ingredients_list: list):
    """
    - This endpoint allows a user to search for recipes based on ingredients they have available on hand and returns
    the recipes in order of highest ingredient match
  - Parameters:
    - ingredients: list of strings (required)
  - Returns List of Recipes: Top 5
    -recipe_name: String
    - user_id : String
    - rating/comments: List
    - total_time: int
    - servings : int
    - spice_level: int
    - cooking_level: int
    - recipe_description: String
    - ingredients: List
    - instructions: List
    """

    return ingredients_list


class recipe_sort_options(str, Enum):
    tags = "tags"
    rating = "rating"
    spiceLevel = "spice_level"
    cookingLevel = "cooking_level"
    servings = "servings"


# Add get parameters
@router.get("/recipes/", tags=["movies"])
def list_recipes(
    tags: str = "",
    rating: int = 0 ,
    spiceLevel : int = 0,
    cookingLevel : int = 0,
    servings : int = 1,
    sort: recipe_sort_options = recipe_sort_options.rating):

    """
      - currently only supports filtering by one tag?
      - This endpoint allows a user to search for recipes based on tags, and sort/filter based on rating.
  - Parameters:
    - id: string (required)
    - tags: string (optional)
    - sort: sort.ratings (optional)
 - Returns a list of recipes  Top 5 based on tags, sorted by rating?
 - Returns List of Recipes: Top 5
    -recipe_name: String
    - user_id : String
    - rating/comments: List
    - total_time: int
    - servings : int
    - spice_level: int
    - cooking_level: int
    - recipe_description: String
    - ingredients: List
    - instructions: List
    """

    return None




