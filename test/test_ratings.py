import sqlalchemy
from fastapi.testclient import TestClient
from src.api.server import app
from src import database as db
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import text

client = TestClient(app)

def test_post_rating1():
    request_body = {
        "username": "post_user",
        "recipe_rating": 5,
        "recipe_comment": "really good recipe",
        "date": date.today().isoformat()
    }
    response = client.post("/recipes/1/rate/", json=request_body)
    assert response.status_code == 200

    conn = db.engine.connect()
    last_rating_id = conn.execute(text(
        "SELECT rating_id FROM recipe_ratings ORDER BY rating_id DESC LIMIT 1"
    )).fetchone()[0]
    assert response.json() == last_rating_id

def test_post_rating2():
    request_body = {
        "username": "testing12345_FAIL!!",
        "recipe_rating": 5,
        "recipe_comment": "really good recipe",
        "date": date.today().isoformat()
    }
    response = client.post("/recipes/1/rate/", json=request_body)
    assert response.status_code == 404

