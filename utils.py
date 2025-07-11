import random
import string

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@yandex.ru"

def generate_user():
    return {
        "email": random_email(),
        "password": "test1234",
        "name": "TestUser"
    }

def register_user(user):
    import requests
    return requests.post(f"{BASE_URL}/auth/register", json=user)

def login_user(user):
    import requests
    return requests.post(f"{BASE_URL}/auth/login", json={
        "email": user["email"],
        "password": user["password"]
    })

def get_access_token(user):
    response = login_user(user)
    return response.json().get("accessToken")

def get_ingredient_ids():
    import requests
    response = requests.get(f"{BASE_URL}/ingredients")
    return [item["_id"] for item in response.json()["data"]]
