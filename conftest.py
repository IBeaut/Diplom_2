import pytest
import requests
from utils import generate_user, BASE_URL

@pytest.fixture
def create_user():
    user = generate_user()
    response = requests.post(f"{BASE_URL}/auth/register", json=user)
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя"
    token = response.json().get("accessToken", "").replace("Bearer ", "")
    user["accessToken"] = token
    return user
