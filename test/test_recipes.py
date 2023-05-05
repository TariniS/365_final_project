from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)

def test_get_recipe():
    response = client.get("/recipes/0")
    assert response.status_code == 200

    with open("test/recipes/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_recipe_2():
    response = client.get("/recipes/400")
    assert response.status_code == 404

