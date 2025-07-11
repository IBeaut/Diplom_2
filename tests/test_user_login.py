import requests
import allure

from utils.helpers import generate_user, register_user
from utils.urls import AUTH_LOGIN
from data.constants import EXPECTED_MESSAGES

@allure.suite("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход в систему")
    def test_login_success(self):
        user = generate_user()
        register_user(user)
        with allure.step("Вход с корректными данными"):
            response = requests.post(AUTH_LOGIN, json={
                "email": user["email"],
                "password": user["password"]
            })
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Ошибка при входе с неверными данными")
    def test_login_invalid_credentials(self):
        with allure.step("Вход с неверным email и паролем"):
            response = requests.post(AUTH_LOGIN, json={
                "email": "wrong@email.com",
                "password": "wrongpass"
            })
        assert response.status_code == 401
        assert response.json()["message"] == EXPECTED_MESSAGES["login_fail"]
