import sqlalchemy
from fastapi.testclient import TestClient
from src.api.server import app
from src import database as db
client = TestClient(app)
def test_post_rating1():
    request_body = {
        "recipe_rating": 9,
        "recipe_comment": "really good recipe",
        "date": "2023-05-07"
    }
    response = client.post("/recipes/0/1/rate/", json=request_body)
    assert response.status_code == 200
    conn = db.engine.connect()
    lastRatingId = conn.execute(
        sqlalchemy.text(
            """SELECT recipe_rating.rating_id FROM recipe_rating
                ORDER BY rating_id DESC LIMIT 1;"""))
    nextRatingId = lastRatingId.fetchone()[0]
    assert response.json() == nextRatingId
def test_post_rating2():
    request_body = {
        "recipe_rating": 9,
        "recipe_comment": "really good recipe",
        "date": "2023-05-07"
    }
    response = client.post("/recipes/100/1/rate/", json=request_body)
    assert response.status_code == 404
def test_post_rating3():
    request_body = {
        "recipe_rating": 9,
        "recipe_comment": "really good recipe",
        "date": "2023-05-07"
    }
    response = client.post("/recipes/0/100/rate/", json=request_body)
    assert response.status_code == 404