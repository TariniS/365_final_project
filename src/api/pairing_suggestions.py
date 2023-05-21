import sqlalchemy
from fastapi import APIRouter, HTTPException
from src import database as db
from sqlalchemy import or_
from typing import List

router = APIRouter()

def get_pairing_suggestions(pairing_type: str, recipe_tags: List[str]):
    stmt = (
        sqlalchemy.select(
            db.recipes.c.recipe_id,
            db.recipes.c.recipe_name
        )
        .select_from(
            db.recipe_tags
            .join(db.recipes)
            .join(db.tags)
        )
        .where(db.recipes.c.recipe_type == pairing_type)
        .where(or_(*[db.tags.c.tag.like(f'%{tag}%') for tag in recipe_tags]))
        .group_by(db.recipes.c.recipe_id, db.recipes.c.recipe_name)
        .order_by(db.recipes.c.recipe_type, db.recipes.c.recipe_name)
)

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        pairing_suggestions = [
            {"recipe_id": row.recipe_id, "recipe_name": row.recipe_name}
            for row in result
        ]

    return pairing_suggestions

@router.get("/recipes/{recipe_id}/pairings", tags=["recipes"])
def recipe_pairing_suggestions(recipe_id: int):

    recipe_type = """SELECT recipes.recipe_type
                        FROM recipes
                        WHERE recipes.recipe_id = :id"""
    recipe_type = db.conn.execute(sqlalchemy.text(recipe_type), {'id': recipe_id}).fetchone()[0]

    recipe_tags = """WITH recipe_tags AS (
                          SELECT recipe_tags.recipe_id,
                                 ARRAY_AGG(tags.tag) AS tags
                          FROM recipe_tags
                          JOIN tags ON recipe_tags.tag_id = tags.tag_id
                          GROUP BY recipe_tags.recipe_id)
                    SELECT tags
                    FROM recipes AS recipe
                    LEFT JOIN recipe_tags ON recipe_tags.recipe_id = recipe.recipe_id
                    WHERE recipe.recipe_id = :id"""
    recipe_tags = db.conn.execute(sqlalchemy.text(recipe_tags), {'id': recipe_id}).fetchone()[0]

    # Define the pairing types based on the recipe type
    if recipe_type == "drink":
        pairing_types = ["food", "dessert"]
    elif recipe_type == "dessert":
        pairing_types = ["drink", "food"]
    elif recipe_type == "food":
        pairing_types = ["drink", "dessert"]
    else:
        raise HTTPException(status_code=400, detail="Invalid recipe type")

    pairing_suggestions = {}

    # Get pairing suggestions based on each pairing type
    for pairing_type in pairing_types:
        suggestions = get_pairing_suggestions(pairing_type, recipe_tags)
        pairing_suggestions[pairing_type] = suggestions

    return {
        "pairing_suggestions": pairing_suggestions
    }