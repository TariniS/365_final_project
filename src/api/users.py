import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db
router = APIRouter()

class UserJSON(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str

@router.post("/users/", tags=["users"])
def add_user(user: UserJSON):
    """
        This endpoint adds a user to Users. The user is represented
        by a user_name which a string representation of the user's name.

        The endpoint returns the id of the resulting user that was created.
        """
    if user.firstname == "" or user.lastname == "" or user.username == "" \
            or user.password == "":
        raise HTTPException(status_code=404, detail="Invalid Name.")

    usercheck = """SELECT COUNT(*) FROM users WHERE username =:input_username"""
    usercheck = db.conn.execute(sqlalchemy.text(usercheck), {'input_username': user.username})
    if usercheck.fetchone()[0] > 0:
        raise HTTPException(status_code=404, detail="Username is taken. Try again")

    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.insert(db.users),
            {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "username": user.username,
                "password": user.password,
            }
        )
    newUserId = db.conn.execute(
        sqlalchemy.text(
            """SELECT user_id FROM users 
            ORDER BY user_id DESC LIMIT 1;""")).fetchone()[0]
    return newUserId
