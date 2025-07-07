import pytest
import requests
from utils import BASE_URL, generate_user, register_user

class TestUserRegistration:

    def test_create_unique_user(self):
        user = generate_user()
        response = register_user(user)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_existing_user(self):
        user = generate_user()
        register_user(user)
        response = register_user(user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_missing_required_fields(self, field):
        user = generate_user()
        user.pop(field)
        response = register_user(user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
