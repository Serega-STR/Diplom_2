class URL:
    BASE_URL = 'https://stellarburgers.education-services.ru/api'

    # EP - ENDPOINT

    CREATE_USER = f'{BASE_URL}/auth/register'      # Регистрация пользователя: POST
    LOGIN_USER = f'{BASE_URL}/auth/login'          # Авторизация пользователя: POST
    
    DELETE_USER = f'{BASE_URL}/auth/user'          # Удаление пользователя: DELETE
                                                # headers={"Authorization": "Bearer {auth_token}"}

    CREATE_ORDER = f'{BASE_URL}/orders'            # POST '/api/orders', payload={ "ingredients": ["...","...", ...] }
                                                # ответ: { "name": "...","order": { "number": 6257 }, "success": true }

