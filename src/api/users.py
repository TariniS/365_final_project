import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
router = APIRouter()

class UserJSON(BaseModel):
    firstname: str
    lastname: str

@router.post("/users/", tags=["users"])
def add_user(user: UserJSON):
    """
        This endpoint adds a user to Users. The user is represented
        by a user_name which a string representation of the user's name.

        The endpoint returns the id of the resulting user that was created.
        """
    if user.firstname == "" or user.lastname == "":
        raise HTTPException(status_code=404, detail="Invalid Name.")

    lastUserId = db.conn.execute(
                    sqlalchemy.text(
                    """SELECT user_id FROM users 
                        ORDER BY user_id DESC LIMIT 1;"""))
    newUserId = lastUserId.fetchone()[0] + 1
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.insert(db.users),
            [
                {
                    "user_id": newUserId,
                    "firstname": user.firstname,
                    "lastname": user.lastname
                }
            ],
        )
    return newUserId
