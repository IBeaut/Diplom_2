import requests
from utils import BASE_URL, generate_user, register_user

class TestUserLogin:

    def test_login_success(self):
        user = generate_user()
        register_user(user)
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        assert response.status_code == 200
        assert "accessToken" in response.json()

    def test_login_invalid_credentials(self):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "wrong@yandex.ru",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
