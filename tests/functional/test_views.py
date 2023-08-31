from src.models import User


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Connectez vous!' in response.data


def test_login_valid_identifiants(client):
    response = client.post('/login', data={"email": "admin@test.com", "password": "admin123"})
    assert response.status_code == 200


def test_login_invalid_password(client):
    response = client.post('/login', data={"email": "test@test.com", "password": ""})
    assert b'Connectez vous!' in response.data


def test_login_inexisting_email(client):
    response = client.post('/login', data={"email": "john@test.com", "password": "admin123"})
    assert b'Connectez vous!' in response.data


def test_register(client, app):
    response = client.post("/register", data={"firstname": "testeur",
                                              "lastname": "tester",
                                              "email": "tester@testing.com",
                                              "password1": "password123",
                                              "password2": "password123"
                                              })

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "tester@testing.com"
        assert response.status_code == 302


def test_projects_page_without_login(client):
    response = client.get("/project")
    assert response.status_code == 302


def test_projects_page_with_login(client):
    client.post("/register", data={"firstname": "testeur",
                                   "lastname": "tester",
                                   "email": "tester@testing.com",
                                   "password1": "password123",
                                   "password2": "password123"
                                   })
    client.post('/login', data={"email": "tester@testing.com", "password": "password123"})
    response = client.get("/project")
    assert b"Gestion projets" in response.data
