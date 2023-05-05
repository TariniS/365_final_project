import sqlalchemy
from fastapi import APIRouter
from pydantic import BaseModel
from src import database as db
router = APIRouter()

class UserJSON(BaseModel):
    user_name: str

@router.post("/users/{user_id}", tags=["users"])
def add_user(user: UserJSON):
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
                    "user_name": user.user_name,
                }
            ],
        )
    return newUserId
