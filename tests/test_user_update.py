import requests
import allure

from utils.helpers import generate_user, register_user, get_access_token
from utils.urls import AUTH_USER
from data.constants import EXPECTED_MESSAGES

@allure.suite("Обновление данных пользователя")
class TestUserUpdate:

    @allure.title("Обновление имени пользователя с авторизацией")
    def test_update_user_with_auth(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        with allure.step("Изменение имени пользователя"):
            response = requests.patch(
                AUTH_USER,
                headers={"Authorization": token},
                json={"name": "NewName"}
            )
        assert response.status_code == 200
        assert response.json()["user"]["name"] == "NewName"

    @allure.title("Попытка обновить данные без авторизации")
    def test_update_user_without_auth(self):
        with allure.step("Запрос на изменение без токена"):
            response = requests.patch(
                AUTH_USER,
                json={"name": "UnauthorizedChange"}
            )
        assert response.status_code == 401
        assert response.json()["message"] == EXPECTED_MESSAGES["unauthorized"]
