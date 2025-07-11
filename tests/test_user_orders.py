import requests
import allure

from utils.helpers import generate_user, register_user, get_access_token, get_ingredient_ids
from utils.urls import ORDERS
from data.constants import EXPECTED_MESSAGES

@allure.suite("Получение заказов пользователя")
class TestUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        ingredient_ids = get_ingredient_ids()

        with allure.step("Создание заказа"):
            requests.post(
                ORDERS,
                headers={"Authorization": token},
                json={"ingredients": ingredient_ids[:2]}
            )

        with allure.step("Получение списка заказов"):
            response = requests.get(ORDERS, headers={"Authorization": token})

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["orders"], list)

    @allure.title("Ошибка при получении заказов без авторизации")
    def test_get_user_orders_unauthorized(self):
        with allure.step("Попытка получить заказы без токена"):
            response = requests.get(ORDERS)

        assert response.status_code == 401
        assert response.json()["message"] == EXPECTED_MESSAGES["unauthorized"]
