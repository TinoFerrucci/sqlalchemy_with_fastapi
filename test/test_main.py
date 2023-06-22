from fastapi.testclient import TestClient
from sqlalchemy_with_fastapi.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_create_user():
    email = "test@example.com"
    password = "test"
    id_user = len(client.get('/users').json()) + 1  # Linea definida para obtener el id del ultimo user agregado

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
    email = "test@example.com"
    password = "test"

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
    id_item = len(client.get("/items").json()) + 1  # Linea definida para obtener el id del ultimo item agregado

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


def get_user_by_id():
    user_id = 1

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
          "email": "constantino@wiener-lab.com",
          "id": 1,
          "is_active": True,
          "items": [
            {
              "title": "Coca Cola",
              "description": "Botella de coca cola",
              "id": 1,
              "owner_id": 1
            },
            {
              "title": "Manaos",
              "description": "Manaos de ciruela",
              "id": 2,
              "owner_id": 1
            }
          ]
        }


def get_user_by_id_non_existent():
    user_id = -1

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }
