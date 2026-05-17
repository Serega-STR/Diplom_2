import pytest
import requests
import allure

from url import URL
from api_methods.order import Order
from api_methods.user import LoginUser as L, TokenUser as T
from data import Data, StatusCodes as code


class TestOrderMethods:
    @allure.title('Успешное создания заказа')
    @allure.description("""Проверка успешного создания заказа
                         с авторизованным пользователем""")
    def test_create_order_by_auth_user_success(self, create_user_scope_function):
        _, payload = create_user_scope_function
        response_auth = L.get_auth(payload)
        access_token = T.get_access_token(response_auth)
        response = Order.create_order(Data.order_payload_valid_id_ingredients, access_token)
        assert response.status_code == code.OK, f'Ошибка! Ожидаемый код статуса {code.OK}, фактический {response.status_code}'
        
        message = response.json()
        
        # основной статус
        assert message["success"] == True

        # наличие основных ключей
        assert 'name' in message 
        assert "order" in message
        assert 'number' in message['order']

        # тип значения у ключа name
        assert type(message['name']) is str
        
        # тип значения у ключа name
        assert type(message['order']['number']) is int


    @allure.title('Ошибка создания заказа')
    @allure.description("""Проверка ошибки  создания заказа
                        с авторизованным пользователем  с неверным хешем ингредиентов""")
    def test_create_order_wrong_id_ingredients_error_message(self, create_user_scope_function):
        _, payload = create_user_scope_function
        response_auth = L.get_auth(payload)
        access_token = T.get_access_token(response_auth)
        response = Order.create_order(Data.order_payload_wrong_id_ingredients, access_token)
        assert response.status_code == code.INT_SERV_ERR, f'Ошибка! Ожидаемый код статуса {code.INT_SERV_ERR}, фактический {response.status_code}'

        
    @allure.title('Ошибка создания заказа')
    @allure.description("""Проверка ошибки создания заказа
                        с авторизованным пользователем  без ингредиентов""")
    def test_create_order_without_ingredients_error_message(self, create_user_scope_function):
        _, payload = create_user_scope_function
        response_auth = L.get_auth(payload)
        access_token = T.get_access_token(response_auth)
        response = Order.create_order(Data.order_payload_without_ingredients, access_token)
        assert response.status_code == code.BAD_REQUEST, f'Ошибка! Ожидаемый код статуса {code.BAD_REQUEST}, фактический {response.status_code}'

        message = response.json()
        
        # основной статус
        assert message["success"] == False
        
        # Общая структура
        assert isinstance(message, dict), "Ответ должен быть словарём"
        assert "success" in message, "В ответе должен быть ключ 'success'"
        assert "message" in message, "В ответе должен быть ключ 'message'"

        # Проверка типов
        assert isinstance(message["success"], bool), "'success' должен быть булевым"
        assert isinstance(message["message"], str), "'message' должен быть строкой"

        # Значения
        assert message["message"] == "Ingredient ids must be provided", "Текст сообщения об ошибке некорректен"


    @allure.title('Ошибка создания заказа')
    @allure.description("""Проверка ошибки создания заказа
                        пользователем без авторизации""")
    def test_create_order_by_unauthorized_user_error_message(self, create_user_scope_function):
        response = Order.create_order(Data.order_payload_valid_id_ingredients)
        assert response.status_code == code.UNAUTHORIZED, f'Ошибка! Ожидаемый код статуса {code.UNAUTHORIZED}, фактический {response.status_code}'
