import requests
from utils import BASE_URL, generate_user, register_user, get_access_token

class TestUserUpdate:

    def test_update_user_with_auth(self):
        user = generate_user()
        register_user(user)
        token = get_access_token(user)
        new_name = "NewName"
        response = requests.patch(f"{BASE_URL}/auth/user",
                                  headers={"Authorization": token},
                                  json={"name": new_name})
        assert response.status_code == 200
        assert response.json()["user"]["name"] == new_name

    def test_update_user_without_auth(self):
        response = requests.patch(f"{BASE_URL}/auth/user", json={"name": "Unauthorized"})
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"
