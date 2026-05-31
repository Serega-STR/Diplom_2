from helper import Generator as G, Helper
from url import URL
from data import *
import allure
import requests


class CreateUser:
    @allure.step("Регистрация нового пользователя")
    def register_new_user(payload=None):
        if payload is None:
            # генерируем логин, пароль и имя пользователя
            payload = G.generate_credentials()

        # отправляем запрос на регистрацию пользователя и сохраняем ответ в переменную response
        response = requests.post(URL.CREATE_USER, data=payload)

        # если регистрация прошла успешно - код ответа 200
        if response.status_code == 200:

            message = response.json()
            Helper.logger.info(f'пользователь создан!\n' + 
                f'payload: {payload}\n' + 
                f'access_token: {message['accessToken']}')
            return response, payload
        else:
            Helper.logger.warning(f'Ошибка! Не удалось создать пользователя: response.status_code == {response.status_code} ')
            return response, payload


class LoginUser:
    @staticmethod
    @allure.step("Авторизация пользователя")
    def get_auth(payload):
        if len(payload) == 3:
            payload = LoginUser.make_payload_for_auth(payload)
        response = requests.post(URL.LOGIN_USER, json=payload)

        if response.status_code == 200:
            Helper.logger.info(f"Пользователь авторизован")
            return response

        else:
            error_message = (
            f"Ошибка АВТОРИЗАЦИИ. "
            f"Статус: {response.status_code} "
            f"Ответ: {response.text}"
        )
            Helper.logger.error(error_message)
            return response

    def make_payload_for_auth(payload):
        new_payload = { 
                        "email": payload["email"],
                        "password": payload["password"]     
                      }
        return new_payload
    
    
class TokenUser:
    @staticmethod
    @allure.step("Получение токена доступа")
    def get_access_token(response):
        Helper.logger.info(f'Достаем токен доступа из response авторизации')
        message = response.json()
        access_token = message['accessToken']
        Helper.logger.info( f'получен токен доступа:\n'+
                            f'access_token: {message['accessToken']}')
        return access_token


class DeleteUser:
    @staticmethod
    @allure.step("Удаление пользователя по токену доступа")    
    def delete_user_by_token(access_token):
        Helper.logger.info(f'удаляем пользователя!')
        response = requests.delete(URL.DELETE_USER, headers={'Authorization': access_token})
        if response.status_code == 202:
            Helper.logger.info(f'Пользователь успешно удален!')
        else:
            Helper.logger.warning('Ошибка! Пользователь не был удален!')
            Helper.logger.warning(f'статус-код {response.status_code}')
            Helper.logger.warning(f'сообщение {response.json()}')
        return response
    

