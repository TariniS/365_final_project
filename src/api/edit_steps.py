from typing import List
import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db

router = APIRouter()

@router.put('/recipes/editStep/', tags=['recipes'])
def edit_step(recipe_id: int, step_order: int, new_step_name: str):


        stepcheck = """SELECT MAX(step_order) FROM instructions WHERE recipe_id =:recipe_id"""
        stepcheck = db.conn.execute(sqlalchemy.text(stepcheck),
                                    {'recipe_id': recipe_id})
        max_step_order = stepcheck.fetchone()[0]
        if step_order > max_step_order:
            raise HTTPException(status_code=404, detail="Invalid step order")

        with db.engine.begin() as conn:
            query = """
                     INSERT INTO instructions (recipe_id, step_order, step_name)
                     VALUES (:recipe_id, :step_order, :step_name)
                     ON CONFLICT (recipe_id, step_order) DO UPDATE
                     SET step_name = EXCLUDED.step_name"""

            conn.execute(sqlalchemy.text(query),
                         {'recipe_id': recipe_id,
                          'step_order': step_order,
                          'step_name': new_step_name})


@router.put('/recipes/addStep/', tags=['recipes'])
def add_step(recipe_id: int, step_order: int, new_step_name: str):
    stepcheck = """
        SELECT MAX(step_order) FROM instructions WHERE recipe_id = :recipe_id
    """
    stepcheck_result = db.conn.execute(sqlalchemy.text(stepcheck), {'recipe_id': recipe_id})
    max_step_order = stepcheck_result.fetchone()[0]

    if step_order > max_step_order + 1:
        raise HTTPException(status_code=404, detail="Invalid step order")

    with db.engine.begin() as conn:
        decrement_query = """
            UPDATE instructions SET step_order = step_order + 1
            WHERE recipe_id = :recipe_id AND step_order > :step_order
        """
        conn.execute(sqlalchemy.text(decrement_query), {'recipe_id': recipe_id, 'step_order': step_order})

        insert_query = """
            INSERT INTO instructions (recipe_id, step_order, step_name)
            VALUES (:recipe_id, :step_order, :step_name)
        """
        conn.execute(
            sqlalchemy.text(insert_query),
            {'recipe_id': recipe_id, 'step_order': step_order, 'step_name': new_step_name}
        )


