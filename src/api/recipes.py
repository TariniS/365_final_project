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
    This endpoint returns a single recipe by its identifier.
    For each recipe it returns:
    * `Recipe Name`: The name of the recipe.
    * `Cooking Time`: The overall rating of the recipe.
    * 'Servings': The total serving size of the recipe
    * `Spice Level`: The spice level of recipe.
    * 'Cooking Level': The cooking level of the recipe
    * 'Description': a short description of the recipe
    * 'Ingredients': list of all ingredients needed for recipe
    * 'Steps': list of instructions for recipe in order
    * 'User Comments': list of comments left by other users for recipe
    """
    stmt = f"""WITH steps AS (
                  select ingredients.recipe_id, 
                  ARRAY_AGG(ingredients.ingredient_name) AS steps
                  from ingredients
                  GROUP BY ingredients.recipe_id),
                comments AS (
                  select recipe_rating.recipe_id, 
                  ARRAY_AGG(recipe_rating.recipe_comment) AS comments
                  from recipe_rating
                  GROUP BY recipe_rating.recipe_id),
                ingre AS (
                  select ingredients.recipe_id, 
                  ARRAY_AGG(ingredients.ingredient_name) AS ingredients
                  from ingredients
                  GROUP BY ingredients.recipe_id)
                SELECT *
                FROM recipe, steps, comments, ingre
                WHERE recipe.recipe_id = {id} AND 
                        recipe.recipe_id = steps.recipe_id AND 
                        recipe.recipe_id = comments.recipe_id and
                        recipe.recipe_id = ingre.recipe_id """

    result = db.conn.execute(sqlalchemy.text(stmt))
    json = []
    for row in result:
        json.append({
            "Recipe Name": row.recipe_name,
            "Cooking Time": row.total_time,
            "Servings": row.servings,
            "Spice Level": row.spicelevel,
            "Cooking Level": row.cookinglevel,
            "Description": row.recipe_description,
            "Ingredients": row.ingredients,
            "Steps": row.steps,
            "User Comments": row.comments
        })
    if json == []:
        raise HTTPException(status_code=404, detail="recipe not found.")
    return json

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
    time = "total_time"
    spiceLevel = "spice_level"
    cookingLevel = "cooking_level"
    servings = "servings"


# Add get parameters
@router.get("/recipes/", tags=["recipes"])
def list_recipes(
        tag: str = "",
        limit: int = 50,
        offset: int = 0,
        sort: recipe_sort_options = recipe_sort_options.time):

    """
    This endpoint returns a list of recipes. For each recipe, it returns:
    * `recipe_id`: the internal id of the recipe. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe name`: The name of the recipe.
    * `Total Time`: The overall rating of the recipe.
    * `Spice Level`: The spice level of recipe.
    * 'Cooking Level': The cooking level of the recipe
    * 'Servings': The total serving size of the recipe

    You can filter for recipes whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `total_time` - Sort by recipe time.
    * `spice_level` - Sort by recipe spice level.
    * `cooking_level` - Sort by recipe cooking level.
    * 'servings' - Sort by recipe servings.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    if sort == recipe_sort_options.time:
        order_by = db.recipes.c.total_time
    elif sort == recipe_sort_options.spiceLevel:
        order_by = db.recipes.c.spicelevel
    elif sort == recipe_sort_options.cookingLevel:
        order_by = db.recipes.c.cookinglevel
    elif sort == recipe_sort_options.servings:
        order_by = db.recipes.c.servings
    else:
        assert False

    stmt = (sqlalchemy.select(
        db.recipes.c.recipe_id,
        db.recipes.c.recipe_name,
        db.recipes.c.total_time,
        db.recipes.c.servings,
        db.recipes.c.spicelevel,
        db.recipes.c.cookinglevel,
        db.recipes.c.recipe_description)
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.recipes.c.recipe_id))

    if tag != "":
        stmt = stmt.where(db.recipes.c.recipe_description.ilike(f"%{tag}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "recipe_id": row.recipe_id,
                    "recipe name": row.recipe_name,
                    "total time": row.total_time,
                    "spice level": row.spicelevel,
                    "cooking level": row.cookinglevel,
                    "servings": row.servings,
                    "description": row.recipe_description
                }
            )

    return json




