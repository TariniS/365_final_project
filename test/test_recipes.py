from fastapi.testclient import TestClient
from src.api.server import app
import json
import sqlalchemy
from src import database as db

client = TestClient(app)

def test_get_recipe():
    response = client.get("/recipes/7")
    assert response.status_code == 200

    with open("test/recipes/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
#
def test_get_recipe_2():
    response = client.get("/recipes/400")
    assert response.status_code == 404


def test_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200

    with open("test/recipes/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
#
#
def test_sort_filter_1():
    response = client.get(
        "/recipes/?tag=nuts"
    )
    assert response.status_code == 200

    with open(
        "test/recipes/name=nuts.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

def test_post_recipe1():
    request_body = {
  "recipe_name": "test",
  "total_time": "string",
  "servings": 0,
  "spice_level": 0,
  "cooking_level": 0,
  "recipe_type": "string",
  "ingredients": [
    {
      "ingredient_name": "string",
      "core_ingredient": "string",
      "quantity": 0,
      "measurement": "string"
    }
  ],
  "instructions": [
    {
      "step_order": 0,
      "step_name": "string"
    }
  ],
  "tags": [
    "string"
  ]
}
    response = client.post("/recipes/testing_user/testing_user/recipe/", json=request_body)
    assert response.status_code == 200
    conn = db.engine.connect()
    lastRecipeId = conn.execute(
        sqlalchemy.text(
            """SELECT recipes.recipe_id FROM recipes
                ORDER BY recipe_id DESC LIMIT 1;"""))
    nextRecipeId = lastRecipeId.fetchone()[0]
    assert response.json() == nextRecipeId
#
def test_post_recipe2():
    # invalid user id
    request_body = {
        "recipe_name": "testing_recipe",
        "total_time": "0 mins",
        "servings": 0,
        "spice_level": 0,
        "cooking_level": 0,
        "recipe_type": "food",
        "ingredients": [
            {"ingredient_name": "test",
             "core_ingredient": "test",
             "quantity": 0,
             "measurement": "test"
             }
        ],
        "instructions": [
            {"step_order": 0,
            "step_name": "test"},
            {"step_order": 1,
             "step_name": "test2"}
        ],
        "tags":["string"]
    }
    response = client.post("/recipes/bad_user/bad_password/recipe/", json=request_body)
    assert response.status_code == 404

