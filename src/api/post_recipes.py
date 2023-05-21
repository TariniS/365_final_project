from typing import List

import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
router = APIRouter()

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
    ingredients: List[Ingredient]
    instructions: List[Instruction]
    tags: List[str]


def upsert_ingredient(ingredient_name: str, core_ingredient: str):
    with db.engine.begin() as conn:
        upsert_query = """
            INSERT INTO ingredients (name, core_ingredient)
            VALUES (:ingredient_name, :core_ingredient)
            ON CONFLICT (name) DO NOTHING
        """

        conn.execute(sqlalchemy.text(upsert_query), {'ingredient_name': ingredient_name, 'core_ingredient': core_ingredient})


def upsert_tags(tag_name: str):
    with db.engine.begin() as conn:
        upsert_query = """
            INSERT INTO tags (tag)
            VALUES (:tag_name)
            ON CONFLICT (tag) DO NOTHING
        """

        conn.execute(sqlalchemy.text(upsert_query), {'tag_name': tag_name})


@router.post("/recipes/{username}/recipe/", tags=["recipes"])
def add_recipe(username: str, recipe: RecipeJson):
    """
    This endpoint adds a recipe to Recipe. The recipe is represented
    by a recipe name, total time, servings, spice level, cooking level
    recipe description, ingredients, and instructions. It also takes in a user_id
    which links the recipe to that specific user.

    The endpoint returns the id of the resulting recipe that was created.
    """

    usercheck = """SELECT COUNT(*) FROM users WHERE username =:user_name"""
    usercheck = db.conn.execute(sqlalchemy.text(usercheck), {'user_name': username}).fetchone()[0]

    if usercheck == 0:
        raise HTTPException(status_code=404, detail="username not found."
                                                    "Please check or create a new user.")

    user_id = """SELECT user_id FROM users WHERE username =:user_name"""
    user_id = db.conn.execute(sqlalchemy.text(user_id),
                              {'user_name': username}).fetchone()[0]

    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.insert(db.recipes),
            [
                {
                    "recipe_name": recipe.recipe_name,
                    "user_id": user_id,
                    "total_time": recipe.total_time,
                    "servings": recipe.servings,
                    "spice_level": recipe.spice_level,
                    "cooking_level": recipe.cooking_level,
                }
            ]
        )

    new_recipe_id = db.conn.execute(
        sqlalchemy.text(
            """SELECT recipe_id FROM recipes 
            ORDER BY recipe_id DESC LIMIT 1;""")).fetchone()[0]

    instruction_values = [
        {
            "recipe_id": new_recipe_id,
            "step_order": currentInstruction.step_order,
            "step_name": currentInstruction.step_name,
        }
        for i, currentInstruction in enumerate(recipe.instructions)
    ]

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.insert(db.instructions), instruction_values)

    for currentIngredient in recipe.ingredients:
        upsert_ingredient(currentIngredient.ingredient_name, currentIngredient.core_ingredient)
        ingredient_id = db.conn.execute(
            sqlalchemy.text(
                "SELECT ingredient_id FROM ingredients WHERE name = :name"
            ),
            {"name": currentIngredient.ingredient_name},
        ).fetchone()[0]

        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.insert(db.recipe_ingredients),
                {
                    "recipe_id": new_recipe_id,
                    "ingredient_id": ingredient_id,
                    "quantity": currentIngredient.quantity,
                    "measurement": currentIngredient.measurement,
                },
            )
    for current_tag in recipe.tags:
        upsert_tags(current_tag)
        tag_id = db.conn.execute(
            sqlalchemy.text(
                "SELECT tag_id FROM tags WHERE tag = :tag"
            ),
            {"tag": current_tag},
        ).fetchone()[0]

        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.insert(db.recipe_tags),
                {
                    "tag_id": tag_id,
                    "recipe_id": new_recipe_id,
                    "tag": current_tag
                },
            )

    return new_recipe_id