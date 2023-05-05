import sqlalchemy
from pydantic import BaseModel
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


@router.get("/findrecipes/", tags=["recipes"])
def get_recipes_by_ingredients(ingredient_list: str):
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

    json = None
    ingredient_list = ingredient_list.split(",")

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


class Ingredient(BaseModel):
    ingredient_name: str
    core_ingredient: str
    quantity: int
    measurement: str


class Instruction(BaseModel):
    step_order: int
    step_name: str


class RecipeJson(BaseModel):
    recipe_name: str
    total_time: str
    servings: int
    spice_level: int
    cooking_level: int
    recipe_description: str
    ingredients: List[Ingredient]
    instructions: List[Instruction]


@router.post("/recipes/{user_id}/recipe/", tags=["movies"])
def add_recipe(user_id: int, recipe: RecipeJson):
    existing_user_query = """ SELECT * 
                              FROM users 
                              WHERE users.user_id = :user_id"""
    existing_user = db.conn.execute(sqlalchemy.text(existing_user_query), {'user_id': user_id})
    last_recipe_id = """ SELECT recipe.recipe_id
                              FROM recipe
                              ORDER BY recipe_id DESC"""
    last_ingredient_id = """ SELECT ingredients.ingredient_id
                              FROM ingredients
                              ORDER BY ingredient_id DESC"""
    last_instruction_id = """ SELECT instructions.instruction_id
                              FROM instructions
                              ORDER BY instruction_id DESC"""
    new_recipe_id = int(db.conn.execute(sqlalchemy.text(last_recipe_id)).first()[0]) + 1
    new_ingredient_id = int(db.conn.execute(sqlalchemy.text(last_ingredient_id)).first()[0]) + 1
    new_instruction_id = int(db.conn.execute(sqlalchemy.text(last_instruction_id)).first()[0]) + 1
    # Error checking
    count = 0
    for row in existing_user:
        count += 1
    if count == 0:
        raise HTTPException(status_code=404, detail="user_id not found. Please create a new user.")
    # user_id valid
    else:
        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.insert(db.recipes),
                [
                    {
                        "recipe_id": new_recipe_id,
                        "recipe_name": recipe.recipe_name,
                        "user_id": user_id,
                        "total_time": recipe.total_time,
                        "servings": recipe.servings,
                        "spicelevel": recipe.spice_level,
                        "cookinglevel": recipe.cooking_level,
                        "recipe_description": recipe.recipe_description
                    }
                ],
            )

            for i in range(len(recipe.ingredients)):
                currentIngredient = recipe.ingredients[i]
                current_ingredient_id = new_ingredient_id + i
                conn.execute(
                    sqlalchemy.insert(db.ingredients),
                    [
                        {
                            "recipe_id": new_recipe_id,
                            "ingredient_id": current_ingredient_id,
                            "ingredient_name": currentIngredient.ingredient_name,
                            "core_ingredient": currentIngredient.core_ingredient,
                            "quantity": currentIngredient.quantity,
                            "measurement": currentIngredient.measurement
                        }
                    ],
                )
            for i in range(len(recipe.instructions)):
                currentInstruction = recipe.instructions[i]
                current_instruction_id = new_instruction_id + i
                conn.execute(
                    sqlalchemy.insert(db.instructions),
                    [
                        {
                            "instruction_id": current_instruction_id,
                            "recipe_id": new_recipe_id,
                            "step_order": currentInstruction.step_order,
                            "step_name": currentInstruction.step_name
                        }
                    ],
                )

    return new_recipe_id
