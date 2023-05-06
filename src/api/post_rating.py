from datetime import datetime, date
from typing import List

import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
router = APIRouter()

class Rating(BaseModel):
    recipe_rating: int
    recipe_comment: str
    date: date


@router.post("/recipes/{user_id}/{recipe_id}/rate/", tags=["recipes"])
def add_rating(user_id: int, recipe_id: int, rating: Rating):
    # add new rating
    # make sure user_id and recipe_id are valid
    # user_id valid
    existing_user_query = """ SELECT *
                                  FROM users 
                                  WHERE users.user_id = :user_id"""
    existing_recipe_query = """SELECT * 
                               FROM recipe
                               WHERE recipe_id = :recipe_id"""

    last_rating_id = """SELECT recipe_rating.rating_id
                        FROM recipe_rating
                        ORDER BY rating_id DESC"""

    existing_user = db.conn.execute(sqlalchemy.text(existing_user_query), {'user_id': user_id})
    existing_recipe = db.conn.execute(sqlalchemy.text(existing_recipe_query), {'recipe_id': recipe_id})
    new_rating_id = int(db.conn.execute(sqlalchemy.text(last_rating_id)).first()[0]) + 1

    count_user = 0
    count_recipe = 0
    for row in existing_user:
        count_user +=1
    for row in existing_recipe:
        count_recipe +=1

    if count_user ==0:
        raise HTTPException(status_code=404, detail="user_id not found. Please create a new user.")
    if count_recipe == 0:
        raise HTTPException(status_code=404, detail="recipe_id not found. Please select an existing recipe.")
    else:
        if count_user !=0 and count_recipe !=0:
            with db.engine.begin() as conn:
                conn.execute(
                    sqlalchemy.insert(db.recipe_rating),
                    [
                        {
                            "rating_id": new_rating_id,
                            "user_id": user_id,
                            "recipe_id": recipe_id,
                            "recipe_rating": rating.recipe_rating,
                            "recipe_comment": rating.recipe_comment,
                            "date": rating.date
                        }
                    ],
                )

    return new_rating_id