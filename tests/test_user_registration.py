import pytest
import requests
import allure

from utils.helpers import generate_user, register_user
from utils.urls import AUTH_REGISTER
from data.constants import EXPECTED_MESSAGES

@allure.suite("Регистрация пользователя")
class TestUserRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    def test_create_unique_user(self):
        user = generate_user()
        with allure.step("Регистрация нового пользователя"):
            response = register_user(user)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self):
        user = generate_user()
        register_user(user)
        with allure.step("Повторная регистрация того же пользователя"):
            response = register_user(user)
        assert response.status_code == 403
        assert response.json()["message"] == EXPECTED_MESSAGES["user_exists"]

    @allure.title("Регистрация без одного из обязательных полей")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_missing_required_fields(self, field):
        user = generate_user()
        user.pop(field)
        with allure.step(f"Регистрация без поля {field}"):
            response = requests.post(AUTH_REGISTER, json=user)
        assert response.status_code == 403
        assert response.json()["message"] == EXPECTED_MESSAGES["missing_fields"]
