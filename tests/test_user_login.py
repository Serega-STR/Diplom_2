import pytest
import requests
import allure
import logging
import string

from url import URL
from api_methods.user import *
from data import Data, StatusCodes as code
from api_methods.user import LoginUser as LU

class TestLoginUser:
    @allure.title('Проверка успешного логина пользователя')
    @allure.description("Пользователь может успешно авторизоваться")
    def test_login_user_success(self, create_user_scope_function): 
        _, payload = create_user_scope_function
        response = LU.get_auth(payload)
        assert response.status_code == 200, f'Ошибка! Ожидаемый код статуса {code.UNAUTHORIZED}, фактический {response.status_code}'
        
        message = response.json()
        
        # Проверяем основной статус
        assert message['success'] == True

        # Проверяем наличие всех необходимых полей
        assert 'success' in message
        assert 'accessToken' in message
        assert 'refreshToken' in message
        assert 'user' in message

        # Проверяем структуру user
        assert 'email' in message['user']
        assert 'name' in message['user']

        # Проверяем типы данных
        assert isinstance(message['accessToken'], str)
        assert isinstance(message['refreshToken'], str)
        assert isinstance(message['user']['email'], str)
        assert isinstance(message['user']['name'], str)

        # Проверяем формат accessToken
        assert message['accessToken'].startswith('Bearer ')

        # Пример проверки конкретных значений (если нужно)
        assert message['user']['email'] == payload[EMAIL]
        assert message['user']['name'] == payload[NAME]

        # Дополнительные проверки
        assert len(message) == 4  # проверяем количество полей в корневом объекте

    @pytest.mark.parametrize('payload', Data.payload_wrong_credentials)
    @allure.title('Проверка входа пользователя с неверными кредами')
    @allure.description(""" Пользователь не может авторизоваться с неверными кредами, 
                            появляется сообщение об ошибке""")
    def test_login(self, create_valid_user, payload):
        response, _ = create_valid_user
        assert response.status_code == code.OK or code.FORBIDDEN, f'Ошибка! Ожидаемый код статуса {code.OK} или {code.FORBIDDEN}, фактический {response.status_code}'
        
        response = LU.get_auth(payload)
        assert response.status_code == code.UNAUTHORIZED, f'Ошибка! Ожидаемый код статуса {code.UNAUTHORIZED}, фактический {response.status_code}'
        
        message = response.json()
        
        # Проверяем основной статус
        assert message['success'] is False
        
        # проверяем содержание сообщения
        assert message['message'] == "email or password are incorrect"
        
        # Убедимся, что в ответе присутствуют оба ожидаемых ключа:
        assert 'success' in message
        assert 'message' in message
        
        #в ответе ровно 2 ключа
        assert len(message) == 2

        # Удостоверимся, что значения имеют ожидаемые типы
        assert isinstance(message['success'], bool)
        assert isinstance(message['message'], str)
        