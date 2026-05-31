from http.client import responses
from json import JSONDecodeError
from custom_requester import CustomRequester
import pytest
import requests

import conftest
from conftest import auth_session, new_booking_data, empty_booking_data
from constants import BASE_URL, BOOKING_ENDPOINT

class TestBookings:
    def test_booking_create(self, requester, booking_data):
        create = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200

    def test_booking_update(self, auth_requester, booking_data, new_booking_data):
        create = auth_requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200
        bookind_id = create.json().get('bookingid')

        response = auth_requester.send_request(
            method='PUT',
            endpoint=BOOKING_ENDPOINT + f'/{bookind_id}',
            data=new_booking_data,
            expected_status=200
        )
        assert response.status_code == 200

    def test_booking_small_update(self, auth_requester, booking_data, small_updated_booking_data):
        create = auth_requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200
        bookind_id = create.json().get('bookingid')

        response = auth_requester.send_request(
            method='PATCH',
            endpoint=BOOKING_ENDPOINT + f'/{bookind_id}',
            data=small_updated_booking_data,
            expected_status=200
        )
        assert response.status_code == 200

    def test_booking_delete(self, auth_requester, booking_data):
        create = auth_requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200
        bookind_id = create.json().get('bookingid')

        response = auth_requester.send_request(
            method='DELETE',
            endpoint=BOOKING_ENDPOINT + f'/{bookind_id}',
            data={},
            expected_status=201
        )
        assert response.status_code == 201

        checking = auth_requester.send_request(
            method='GET',
            endpoint=BOOKING_ENDPOINT + f'/{bookind_id}',
            data={},
            expected_status=404
        )
        assert checking.status_code == 404

    def test_booking_get(self, requester):
        response = requester.send_request(
            method='GET',
            endpoint=BOOKING_ENDPOINT,
            data={},
            expected_status=200
        )
        assert response.status_code == 200

    def test_booking_get_id(self, requester, booking_data):
        create = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200
        bookind_id = create.json().get('bookingid')

        response = requester.send_request(
            method='GET',
            endpoint=BOOKING_ENDPOINT + f'/{bookind_id}',
            data={},
            expected_status=200
        )
        assert response.status_code == 200

class TestBookingsNegative:
    def test_booking_create_neg(self, requester, negative_booking_data):
        response = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=negative_booking_data,
            expected_status=500
        )
        assert response.status_code == 500
    def test_booking_update_neg(self, auth_requester, new_booking_data):
        """ПОПЫТКА ОБНОВЛЕНИЯ ПО НЕСУЩЕСТВУЮЩЕМУ ID"""
        response = auth_requester.send_request(
            method='PUT',
            endpoint=BOOKING_ENDPOINT + '/____invalid_id____',
            data=new_booking_data,
            expected_status=405
        )
        assert response.status_code == 405, 'Метод выполним'

    def test_booking_small_update_neg(self, auth_requester,booking_data, empty_booking_data):
        create = auth_requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200

        booking_id = create.json().get('bookingid')
        response = auth_requester.send_request(
            method='PATCH',
            endpoint=BOOKING_ENDPOINT + f'/{booking_id}',
            data=empty_booking_data,
            expected_status=400
        )
        assert response.status_code == 400
        """БАГ: ОБНОВЛЕНИЕ С ПУТЫМИ ДАННЫМИ"""
        assert response.json()['firstname'] != ''
        assert response.json()['additionalneeds'] != ''

    def test_booking_get_neg(self, requester):
        """ПОПЫТКА ВЗЯТЬ ДАННЫЕ НЕСУЩЕСТВУЮЩЕГО РЕСУРСА"""
        negative_booking_id = '8924qw89a189f1389df481'
        response = requester.send_request(
            method='GET',
            endpoint=BOOKING_ENDPOINT + f'/{negative_booking_id}',
            data={},
            expected_status=404
        )
        assert response.status_code == 404, 'РЕСУРС НАЙДЕН'

    def test_booking_delete_neg(self, requester, booking_data):
        create = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        assert create.status_code == 200

        booking_id = create.json().get('bookingid')
        '''ПОПЫТКА УДАЛИТЬ СОЗДАННУЮ БРОНЬ БЕЗ АВТОРИЗАЦИИ'''
        response = requester.send_request(
            method='DELETE',
            endpoint=BOOKING_ENDPOINT + f"/{booking_id}",
            data={},
            expected_status=403
        )
        assert response.status_code == 403





