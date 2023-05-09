from fastapi.testclient import TestClient
from src.api.server import app
import json
import sqlalchemy
from src import database as db

client = TestClient(app)

def test_get_recipe():
    response = client.get("/recipes/0")
    assert response.status_code == 200

    with open("test/recipes/0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_recipe_2():
    response = client.get("/recipes/400")
    assert response.status_code == 404

def test_get_recipe_from_ingredients():
    response = client.get("/findrecipes/?ingredient_list=cheese,bread")
    assert response.status_code == 200
    with open("test/findrecipes/ingredientsList.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_recipe_from_ingredients_1():
    response = client.get("/findrecipes/?ingredient_list=bread")
    assert response.status_code == 200
    with open("test/findrecipes/ingredientsList2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200

    with open("test/recipes/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_sort_filter():
    response = client.get(
        "/recipes/?sort=total_time"
    )
    assert response.status_code == 200

    with open(
        "test/recipes/sort=total_time.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

def test_sort_filter_1():
    response = client.get(
        "/recipes/?tag=quick"
    )
    assert response.status_code == 200

    with open(
        "test/recipes/name=quick.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

def test_sort_filter_2():
    response = client.get(
        "/recipes/?sort=servings"
    )
    assert response.status_code == 200

    with open(
        "test/recipes/sort=servings.json",
        encoding="utf-8",
    ) as f:
        assert response.json() == json.load(f)

def test_post_recipe1():
    request_body = {
        "recipe_name": "testing_recipe",
        "total_time": "0 mins",
        "servings": 0,
        "spice_level": 0,
        "cooking_level": 0,
        "recipe_description": "this is a test",
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
        ]
    }
    response = client.post("/recipes/0/recipe/", json=request_body)
    assert response.status_code == 200
    conn = db.engine.connect()
    lastRecipeId = conn.execute(
        sqlalchemy.text(
            """SELECT recipe.recipe_id FROM recipe
                ORDER BY recipe_id DESC LIMIT 1;"""))
    nextRecipeId = lastRecipeId.fetchone()[0]
    assert response.json() == nextRecipeId

def test_post_recipe2():
    # invalid user id
    request_body = {
        "recipe_name": "testing_recipe",
        "total_time": "0 mins",
        "servings": 0,
        "spice_level": 0,
        "cooking_level": 0,
        "recipe_description": "this is a test",
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
        ]
    }
    response = client.post("/recipes/100/recipe/", json=request_body)
    assert response.status_code == 404


