import random
import string
import requests
from utils.urls import AUTH_REGISTER, AUTH_LOGIN, INGREDIENTS

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@yandex.ru"

def generate_user():
    return {
        "email": random_email(),
        "password": "test1234",
        "name": "TestUser"
    }

def register_user(user):
    return requests.post(AUTH_REGISTER, json=user)

def login_user(user):
    return requests.post(AUTH_LOGIN, json={
        "email": user["email"],
        "password": user["password"]
    })

def get_access_token(user):
    response = login_user(user)
    return response.json().get("accessToken")

def get_ingredient_ids():
    response = requests.get(INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]
