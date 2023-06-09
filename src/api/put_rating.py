# from datetime import datetime, date
#
# from typing import List
#
# import sqlalchemy
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from sqlalchemy.exc import IntegrityError
#
# from src import database as db
# router = APIRouter()
#
# class Rating(BaseModel):
#     username: str
#     recipe_rating: int
#     recipe_comment: str
#     date: date
#
# @router.put("/recipes/{recipe_id}/rate/", tags=["recipes"])
# def update_rating(recipe_id: int, rating: Rating):
#     """
#     This endpoint updates a rating provided using the rating_id argument.
#     The rating is represented by a recipe rating, recipe comment, and the
#     date when the rating was added. It also takes in a user_id and
#     recipe_id to ensure that the rating is added by the specific user and
#       to the desired recipe they would like to rate.
#
#     The endpoint returns the id of the recipe rating that was modified.
#     """
#     usercheck = """SELECT COUNT(*) FROM users WHERE username =:user_name"""
#     usercheck = db.conn.execute(sqlalchemy.text(usercheck),
#                                 {'user_name': rating.username}).fetchone()[0]
#
#     if usercheck == 0:
#         raise HTTPException(status_code=404, detail="username not found. "
#                                                     "Please check or create new user.")
#
#     user_id = """SELECT user_id FROM users WHERE username =:user_name"""
#     user_id = db.conn.execute(sqlalchemy.text(user_id),
#                               {'user_name': rating.username}).fetchone()[0]
#
#     existing_rating_query = """
#             SELECT rating_id
#             FROM recipe_ratings
#             WHERE recipe_id = :recipe_id AND user_id = :user_id
#         """
#     existing_rating_result = db.conn.execute(
#         sqlalchemy.text(existing_rating_query),
#         {"recipe_id": recipe_id, "user_id": user_id}
#     ).fetchone()
#
#     if not existing_rating_result:
#         raise HTTPException(status_code=404, detail="No existing rating found. Please create a new rating.")
#
#     with db.engine.begin() as conn:
#         try:
#             conn.execute(
#                 sqlalchemy.update(db.recipe_rating).where(db.recipe_rating.c.recipe_id == recipe_id),
#                 [
#                     {
#                         "user_id": user_id,
#                         "recipe_id": recipe_id,
#                         "recipe_rating": rating.recipe_rating,
#                         "recipe_comment": rating.recipe_comment,
#                         "date": rating.date
#                     }
#                 ],
#             )
#         except IntegrityError as e:
#             error_msg = str(e)
#             if 'recipe_rating_recipe_id_fkey' in error_msg:
#                 raise HTTPException(status_code=404, detail="Invalid recipe_id.")
#             elif 'recipe_rating_user_id_fkey' in error_msg:
#                 raise HTTPException(status_code=404, detail="Invalid user_id.")
#             elif 'recipe_rating_rating_id_pkey' in error_msg:
#                 raise HTTPException(status_code=404, detail="Invalid rating_id.")
#
#     new_rating_id = db.conn.execute(
#         sqlalchemy.text(
#             """SELECT rating_id FROM recipe_ratings
#             ORDER BY rating_id DESC LIMIT 1;""")).fetchone()[0]
#
#     return new_rating_id