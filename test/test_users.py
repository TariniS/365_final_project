# from fastapi.testclient import TestClient
# from src.api.server import app
# from src import database as db
# import sqlalchemy
#
# client = TestClient(app)
#
# def test_post_1():
#     response = client.post("/users/", json={
#                            "firstname": "post_user",
#                            "lastname": "post_user",
#                             "username": "post_user",
#                            "password": "post_user"
#     })
#     assert response.status_code == 200
#     conn = db.engine.connect()
#     lastUserId = conn.execute(
#         sqlalchemy.text(
#             """SELECT user_id FROM users
#                 ORDER BY user_id DESC LIMIT 1;"""))
#     newUserId = lastUserId.fetchone()[0]
#     assert response.json() == newUserId
#
# def test_post_2():
#     response = client.post("/users/", json={
#                           "firstname" : "",
#                            "lastname": "",
#                             "username": "",
#                            "password": ""})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Invalid Name."}
