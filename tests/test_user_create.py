import pytest
import requests
import allure
import logging
import string

from url import URL
from api_methods.user import *
from data import Data, StatusCodes as code
from api_methods.user import CreateUser as CU

class TestUser:
    @allure.title('Создание пользователя')
    @allure.description("Проверка успешного создания пользователя")
    def test_create_user_success(self, create_user_scope_function):
        response, _ = create_user_scope_function
        assert response.status_code == code.OK, f'Ошибка! Ожидаемый код статуса {code.OK}, фактический {response.status_code}'

        message = response.json()

        # Проверяем основной статус
        assert message['success'] == True

        # проверка длины и типа сообщения
        assert isinstance(message, dict), f"Ошибка! Ответ не является словарем, тип: {type(message).__name__}"
        assert len(message) == 4, f"Ошибка! Ожидаемая длина словаря == 4. Фактическая: {len(message)}"

        # Проверяем наличие всех необходимых полей
        assert 'user' in message
        assert 'accessToken' in message
        assert 'refreshToken' in message

        # Проверяем структуру user
        assert 'email' in message['user']
        assert 'name' in message['user']

        # Проверяем типы данных
        assert isinstance(message['accessToken'], str)
        assert isinstance(message['refreshToken'], str)
        assert isinstance(message['user']['email'], str)
        assert isinstance(message['user']['name'], str)


    @allure.title('Создание дубликата пользователя')
    @allure.description("Проверка создания дубликата пользователя, возникает ошибка")
    def test_create_user_duplicate_check_error_message(self, create_user_scope_function):
        _, payload = create_user_scope_function
        response, _ = CU.register_new_user(payload)
        assert response.status_code == code.FORBIDDEN, f'Ошибка! Ожидаемый код статуса {code.FORBIDDEN}, фактический {response.status_code}'

        message = response.json()

        # Проверяем основной статус
        assert message['success'] == False

        # Проверяем наличие всех необходимых полей
        assert 'success' in message
        assert 'message' in message

        # Проверяем тип данных
        assert isinstance(message['message'], str)

        # Проверяем конкретное сообщение об ошибке
        assert message['message'] == "User already exists"

        # проверяем, что в ответе только два поля
        assert len(message) == 2  




    @pytest.mark.parametrize('payload', Data.payload_with_empty_field)
    @allure.title('Нельзя создать пользователя с пустым полем')
    @allure.description("""Нельзя создать пользователя, если одного из полей нет. 
                        Запрос возвращает ошибку""")
    def test_create_user_with_empty_field_check_error_message(self, payload):
        response, _ = CU.register_new_user(payload)
        assert response.status_code == code.FORBIDDEN, f'Ошибка! Ожидаемый код статуса {code.FORBIDDEN}, фактический {response.status_code}'
        
        message = response.json()
        
        # Проверяем основной статус
        assert message['success'] == False

        # Проверяем наличие всех необходимых полей
        assert 'success' in message
        assert 'message' in message

        # Проверяем тип данных
        assert isinstance(message['message'], str)

        # Проверяем точное соответствие текста ошибки
        assert message['message'] == "Email, password and name are required fields"

        # Дополнительные проверки:
        # проверяем, что в ответе только два поля
        assert len(message) == 2

