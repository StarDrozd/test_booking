import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL
from custom_requester import CustomRequester

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture
def requester():
    session = requests.session()
    return CustomRequester(session, BASE_URL)

@pytest.fixture
def auth_requester(auth_session):
    session = auth_session
    return CustomRequester(session, BASE_URL)

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def new_booking_data():
    return {
        "firstname": 'Sasha',
        "lastname": 'Drozdov',
        "totalprice": 555,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Beer"
    }

@pytest.fixture
def small_updated_booking_data():
    return {
        'firstname': 'Alex',
        'additionalneeds': 'Juice'
    }

@pytest.fixture
def negative_booking_data():
    return {
        "firstname": 123,
        "lastname": 'Galitskiy',
        "totalprice": 555,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def empty_booking_data():
    return {
        'firstname': '',
        'additionalneeds': ''
    }
