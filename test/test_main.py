from fastapi.testclient import TestClient
from sqlalchemy_with_fastapi.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_create_user():
    email = "test1123456@example.com"
    password = "test1"
    id_user = len(client.get('/users').json()) + 1 #Linea definida para obtener el id del ultimo user agregado

    response = client.post(
        "/users",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
          "email": email,
          "id": id_user,
          "is_active": True,
          "items": []
            }


def test_user_already_created():
    email = "test1123@example.com"
    password = "test1"

    response = client.post(
        "/users",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
          "detail": "Email already registered"
            }


def test_item_create():
    user_id = 2
    title = ""
    description = ""
    id_item = len(client.get("/items").json()) + 1 #Linea definida para obtener el id del ultimo item agregado

    response = client.post(
        f"/users/{user_id}/items",
        json={
            "title": title,
            "description": description,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": title,
        "description": description,
        "id": id_item,
        "owner_id": user_id
            }


def