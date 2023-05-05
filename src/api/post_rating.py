from datetime import datetime
from typing import List

import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
router = APIRouter()

class Rating(BaseModel):
    recipe_rating: int
    recipe_comment: str
    date: datetime.date


@router.post("/recipes/{user_id}/{recipe_id}/rate/", tags=["movies"])
def add_rating(user_id: int, recipe_id: int, rating: Rating):
    # add new rating


    return 0;