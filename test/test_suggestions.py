from fastapi.testclient import TestClient
from src.api.server import app
from src import database as db
import sqlalchemy

client = TestClient(app)

def test_recipe_pairing_suggestions():
    # Test case 1: Valid recipe pairing
    response = client.get("/recipes/8/pairings")
    assert response.status_code == 200
    assert "pairing_suggestions" in response.json()

def test_recipe_pairing_suggestions_2():
    # Test case 2: Invalid recipe_id
    response = client.get("/recipes/100/pairings")
    assert response.status_code == 404


