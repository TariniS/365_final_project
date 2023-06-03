from datetime import datetime, date

from typing import List

import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from src import database as db
router = APIRouter()

class Rating(BaseModel):
    password: str
    recipe_rating: int
    recipe_comment: str
    date: date


@router.post("/recipes/{recipe_id}/rate/", tags=["recipes"])
def add_rating(recipe_id: int, username: str, rating: Rating):
    """
    This endpoint adds a rating to a Recipe. The rating is represented
    by a recipe rating, recipe comment, and the date when the rating was added.
    It also takes in a user_id and recipe_id to ensure that the rating is added
    by the specific user and to the desired recipe they would like to rate.

    The endpoint returns the id of the recipe rating that was created.
    """
    usercheck = """SELECT COUNT(*) FROM users WHERE username =:user_name"""
    usercheck = db.conn.execute(sqlalchemy.text(usercheck),
                                {'user_name': username}).fetchone()[0]

    if usercheck == 0:
        raise HTTPException(status_code=404, detail="username not found. "
                                                    "Please check or create new user.")

    user_info = db.conn.execute(
        sqlalchemy.text("SELECT user_id, password FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()

    stored_password = user_info[1]
    password_match_query = """
               SELECT crypt(:password, :stored_password) = :stored_password AS password_match;
           """
    password_match = db.conn.execute(
        sqlalchemy.text(password_match_query),
        {
            "password": rating.password,
            "stored_password": stored_password,
        }
    ).fetchone()

    if not password_match[0]:
        raise HTTPException(status_code=401, detail="Invalid password. Access denied.")

    user_id = """SELECT user_id FROM users WHERE username =:user_name"""
    user_id = db.conn.execute(sqlalchemy.text(user_id),
                              {'user_name': username}).fetchone()[0]

    recipecheck = """SELECT COUNT(*) FROM recipes WHERE recipe_id =:recipe_id"""
    recipecheck = db.conn.execute(sqlalchemy.text(recipecheck),
                                {'recipe_id': recipe_id}).fetchone()[0]

    if recipecheck == 0:
        raise HTTPException(status_code=404, detail="Recipe not found. "
                                                    "Please check.")

    with db.engine.begin() as conn:
        try:
            conn.execute(
                sqlalchemy.insert(db.recipe_rating),
                [
                    {
                        "user_id": user_id,
                        "recipe_id": recipe_id,
                        "recipe_rating": rating.recipe_rating,
                        "recipe_comment": rating.recipe_comment,
                        "date": rating.date
                    }
                ],
            )
        except IntegrityError as e:
            error_msg = str(e)
            if 'recipe_rating_recipe_id_fkey' in error_msg:
                raise HTTPException(status_code=404, detail="Invalid recipe_id.")
            elif 'recipe_rating_user_id_fkey' in error_msg:
                raise HTTPException(status_code=404, detail="Invalid user_id.")

    new_rating_id = db.conn.execute(
        sqlalchemy.text(
            """SELECT rating_id FROM recipe_ratings
            ORDER BY rating_id DESC LIMIT 1;""")).fetchone()[0]

    return new_rating_id