from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to School API"

# def test_sign_up():
#     response = client.post(
#         "/auth/sign_up",
#         headers={"accept": "application/json", "Content-Type": "application/json"},
#         json={"id": 200, "username": "Foo Bar", "password": "The Foo Barters"},
#     )
#     assert response.status_code == 200
#     assert response.json()["msg"] == "User creation succeeded"
#     assert "token" in response.json()

# def test_sign_up_existing():
#     response = client.post(
#         "/auth/sign_up",
#         headers={"accept": "application/json", "Content-Type": "application/json"},
#         json={"id": 200, "username": "Foo Bar", "password": "The Foo Barters"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "username is taken"}