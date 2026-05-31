import requests
import allure

from url import URL
from helper import Helper as H

class Order:
    @staticmethod
    @allure.step("Создаем заказ")
    def create_order(payload, access_token=None):
        if access_token is None:
            response = requests.post(URL.CREATE_ORDER, json=payload)
        else:
            response = requests.post(URL.CREATE_ORDER, json=payload, headers={'Authorization': access_token})
        
        if response.status_code == 200:
            H.logger.info('Успешное создание заказа')
        else:
            H.logger.warning(f'Не удалось создать заказ. status_code == {response.status_code}')
        return response


    @staticmethod
    @allure.step("Получаем список ингредиентов")
    def get_list_of_ingredients(payload=None):
        response = requests.get(URL.GET_INGREDIENTS, json=payload)
        if response.status_code == 200:
            logger.info('Получен список ингредиентов')
        else:
            logger.warning(f'Не удалось получить список ингредиентов. status_code == {response.status_code}')
        return response