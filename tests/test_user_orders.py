import requests
from utils import BASE_URL, generate_user, register_user, get_access_token, get_ingredient_ids

class TestUserOrders:

    def test_get_user_orders_authorized(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        ingredient_ids = get_ingredient_ids()
        # создать заказ
        requests.post(f"{BASE_URL}/orders",
                      headers={"Authorization": token},
                      json={"ingredients": ingredient_ids[:2]})
        # получить заказы
        response = requests.get(f"{BASE_URL}/orders",
                                headers={"Authorization": token})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["orders"], list)

    def test_get_user_orders_unauthorized(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
