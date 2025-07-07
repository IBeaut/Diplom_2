import requests
from utils import BASE_URL, generate_user, register_user, get_access_token, get_ingredient_ids

class TestOrderCreation:

    def test_create_order_authorized(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        ingredient_ids = get_ingredient_ids()
        response = requests.post(f"{BASE_URL}/orders",
                                 headers={"Authorization": token},
                                 json={"ingredients": ingredient_ids[:2]})
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_unauthorized(self):
        ingredient_ids = get_ingredient_ids()
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ingredient_ids[:2]})
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_without_ingredients(self):
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": []})
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    def test_create_order_with_invalid_ingredient(self):
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ["invalid_hash"]})
        assert response.status_code == 500
