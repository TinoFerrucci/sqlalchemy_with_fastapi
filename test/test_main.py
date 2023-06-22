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


def test_delete_user():
    user_id = len(client.get('/users').json())
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 201
    assert response.json() == {
          "message": "User deleted"
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


def test_get_user_by_id():
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


def test_get_user_by_id_non_existent():
    user_id = -1

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_get_items_by_user_id():
    user_id = 1

    response = client.get(f"/items/{user_id}")

    assert response.status_code == 200
    assert response.json() == [
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


def test_get_items_by_user_id_non_existent():
    user_id = -1

    response = client.get(f"/items/{user_id}")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_item():
    item_id = len(client.get(f"/items").json())

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 201
    assert response.json() == {
        "message": "Item deleted"
    }


def test_delete_item_not_exist():
    item_id = -1

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Item not found"
    }


def test_user_login_wrong_password():
    email = "constantino@wiener-lab.com"
    password = "some_wrong_password"

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invalid credentials"
    }


def test_user_login_good_password():
    email = "constantino@wiener-lab.com"
    password = "123456"

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 202
    assert response.json() == {
        "message": "User successfully logged"
    }