from fastapi.testclient import TestClient
from src.api.server import app
from src import database as db
import sqlalchemy
import json

client = TestClient(app)

def test_find_recipe():
    response = client.get("/findrecipes/?ingredient_list=chocolate")
    assert response.status_code == 200
    with open("test/findrecipes/ingredientsList.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_find_recipe_2():
    response = client.get("/findrecipes/?ingredient_list=sprinkles")
    assert response.status_code == 200
    with open("test/findrecipes/ingredientsList2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)



