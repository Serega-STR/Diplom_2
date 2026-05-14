
class URL:
    BASE_URL = 'https://stellarburgers.education-services.ru/api'

    # EP - ENDPOINT

    CREATE_USER = f'{BASE_URL}/auth/register'      # Регистрация пользователя: POST
    LOGIN_USER = f'{BASE_URL}/auth/login'          # Авторизация пользователя: POST
    
    DELETE_USER = f'{BASE_URL}/auth/user'          # Удаление пользователя: DELETE
                                                # headers={"Authorization": "Bearer {auth_token}"}
    GET_USER_DATA = f'{BASE_URL}/auth/user'        # Получение данных пользователя: GET
    UPDATE_USER = f'{BASE_URL}/auth/user'          # Обновление данных пользователя: PATCH
    GET_INGREDIENTS = f'{BASE_URL}/ingredients'    # GET
                                                # ответ: {'success': True, 'data': [{...}, ... ]

    CREATE_ORDER = f'{BASE_URL}/orders'            # POST '/api/orders', payload={ "ingredients": ["...","...", ...] }
                                                # ответ: { "name": "...","order": { "number": 6257 }, "success": true }

    GET_USER_ORDERS = f'{BASE_URL}/orders'         # GET (50 последних заказов)

    RESET_PASSWORD = f'{BASE_URL}/password-reset/reset'    # POST '/api/password-reset/reset'
                                                # { "password": "", "token": "" }

    UPDATE_TOKEN = f'{BASE_URL}/auth/token'        # Обновление токена: POST

    LOGOUT_USER = f'{BASE_URL}/auth/logout'        # Выход из системы: POST, body={"token": "{{refreshToken}}"}

