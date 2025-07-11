import pytest
import requests
import allure

from utils.helpers import generate_user, register_user, get_access_token, get_ingredient_ids
from utils.urls import ORDERS
from data.constants import EXPECTED_MESSAGES

@allure.suite("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authorized(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        ingredient_ids = get_ingredient_ids()

        with allure.step("Отправка POST-запроса на создание заказа с токеном"):
            response = requests.post(
                ORDERS,
                headers={"Authorization": token},
                json={"ingredients": ingredient_ids[:2]}
            )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized(self):
        ingredient_ids = get_ingredient_ids()

        with allure.step("Отправка запроса без токена"):
            response = requests.post(
                ORDERS,
                json={"ingredients": ingredient_ids[:2]}
            )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        with allure.step("Отправка запроса с пустым списком ингредиентов"):
            response = requests.post(ORDERS, json={"ingredients": []})

        assert response.status_code == 400
        assert response.json()["message"] == EXPECTED_MESSAGES["missing_ingredients"]

    @allure.title("Создание заказа с невалидным ингредиентом")
    def test_create_order_with_invalid_ingredient(self):
        with allure.step("Отправка запроса с некорректным ID ингредиента"):
            response = requests.post(ORDERS, json={"ingredients": ["invalid_hash"]})

        assert response.status_code == 500
