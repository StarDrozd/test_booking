from json import JSONDecodeError

import pytest
import requests

import conftest
from conftest import auth_session
from constants import BASE_URL

class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        '''# Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"'''

    def test_update_booking(self, auth_session, booking_data, new_booking_data):

        '''ШАГ 1 СОЗДАТЬ БРОНЬ + ПРОВЕРКИ'''
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        '''ШАГ 2 ВЫПОЛНИТЬ PUT С ОБНОВЛЕННЫМ ДАННЫМИ'''
        update_booking = auth_session.put(f'{BASE_URL}/booking/{booking_id}', json=new_booking_data)
        assert update_booking.status_code == 200, 'Ошибка обновления'

        '''ШАГ 3 ПОЛОЧИТЬ ОБНОВЛЕННУЮ БРОНЬ'''
        get_new_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")

        '''ШАГ 4 ПРОВЕРКИ ЧТО ДАННЫЕ ОБНОВИЛИСЬ'''
        assert get_new_booking.status_code == 200, 'Бронь не найдена'
        assert get_new_booking.json()['lastname'] != get_booking.json()["lastname"], 'Фамилия не обновилась'
        assert get_new_booking.json()['firstname'] != get_booking.json()["firstname"], 'Имя не обновилось'

    def test_small_update_booking(self, auth_session, booking_data, small_updated_booking_data):
        '''ШАГ 1 СОЗДАТЬ БРОНЬ + ПРОВЕРКИ'''
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        '''ШАГ 2 ВЫПОЛНИТЬ PATCH С ОБНОВЛЕННЫМ ДАННЫМИ'''
        small_update_booking = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json=small_updated_booking_data)
        assert small_update_booking.status_code == 200, 'Ошибка обновления'

        '''ШАГ 3 ПОЛОЧИТЬ ОБНОВЛЕННУЮ БРОНЬ + ПРОВЕРКИ ОБНОВЛЕННЫХ ДАННЫХ'''
        get_updated_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_updated_booking.status_code == 200, 'Бронь не найдена'
        assert get_updated_booking.json()['additionalneeds'] != get_booking.json()["additionalneeds"], 'Пожелания не обновилась'
        assert get_updated_booking.json()['firstname'] != get_booking.json()["firstname"], 'Имя не обновилось'

    def test_negative_create_booking(self, auth_session, negative_booking_data):
        negative_create_booking = auth_session.post(f'{BASE_URL}/booking', json=negative_booking_data)
        assert negative_create_booking.status_code == 500, 'Ошибка валдиации данных'

    def test_negative_update_booking(self, auth_session, new_booking_data):
        '''ПОПЫТКА ОБНОВИТЬ БРОНЬ ПО НЕВЕРНОМУ URL'''
        negative_update_booking = auth_session.put(f'{BASE_URL}/booking/jopa', json=new_booking_data)
        assert negative_update_booking.status_code == 405, 'Метод выполним'

    def test_negative_small_update_booking(self, auth_session,booking_data):
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        assert create_booking.status_code == 200, 'Бронь не создана'
        booking_id = create_booking.json().get('bookingid')
        get_bokking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')

        '''ПОПЫТКА ОБНОВИТЬ С ПУСТЫНМИ ДАННЫМИ'''
        negative_small_update_booking = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json={})
        assert negative_small_update_booking.status_code == 200, 'Бронь не создана'

        negative_get_small_update_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert negative_get_small_update_booking.json()['firstname'] == get_bokking.json()['firstname'], 'Данные стали пустыми'


    def test_negative_get_booking(self, auth_session):
        '''ПОПЫТКА ВЗЯТЬ ДАННЫЕ НЕСУЩЕСТВУЮЩЕГО РЕСУРСА'''
        negative_booking_id = 8924891891389481
        negative_get_booking = auth_session.get(f'{BASE_URL}/booking/{negative_booking_id}')
        assert negative_get_booking.status_code == 404, 'РЕСУРС НАЙДЕН'

    def test_negative_deelete_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        assert create_booking.status_code == 200, 'Бронь не создана'
        booking_id = create_booking.json().get('bookingid')

        '''ПОПЫТКА УДАЛИТЬ СОЗДАННУЮ БРОНЬ БЕЗ АВТОРИЗАЦИИ'''
        negative_delete_booking = requests.delete(f'{BASE_URL}/booking/{booking_id}')
        assert negative_delete_booking.status_code == 403





