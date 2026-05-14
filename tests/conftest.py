import logging
import pytest
import requests

from data import Data
from url import *
from api_methods.user import CreateUser as C, TokenUser as T, LoginUser as L, DeleteUser as D
    
# Создаём функцию‑фабрику, которая возвращает фикстуру с нужными параметрами:
def _make_user_fixture(scope, payload=None):
    @pytest.fixture(scope=scope)
    def _user_fixture(received_payload=payload):
        response, used_payload = C.register_new_user(received_payload)

        yield response, used_payload

        # Очистка после теста
        response = L.get_auth(used_payload)
        access_token = T.get_access_token(response)
        D.delete_user_by_token(access_token)
    return _user_fixture

# Создаём конкретные фикстуры на основе фабрики
create_user_scope_function = _make_user_fixture('function')
create_user_scope_class = _make_user_fixture('class')
create_valid_user = _make_user_fixture('class', Data.payload_valid)