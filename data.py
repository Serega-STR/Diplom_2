EMAIL = "email"
PASSWORD = "password"
NAME = "name"

class Data:
    # заведомо валидные данные, позволяющие создать пользователя
    
    domen = '@yandex.ru'
    post_name = 'vasya2_test-data'
    email = post_name + domen
    password = 'password'
    name = 'name'

    payload_valid = {
        EMAIL   : email, 
        PASSWORD: password,
        NAME    : name
                    }
    
    # полезная нагрузка с пустыми полями (комбинации)
    payload_with_empty_field = [
        # fully valid example {EMAIL: email, PASSWORD: password, NAME: name}

        # one field empty string
        {EMAIL: '', PASSWORD: password, NAME: name},                        # 0
        {EMAIL: email, PASSWORD: '', NAME: name},                           # 1 
        {EMAIL: email, PASSWORD: password, NAME: ''},                       # 2

        # one field is None       
        {EMAIL: None, PASSWORD: password, NAME: name},                      # 3 
        {EMAIL: email, PASSWORD: None, NAME: name},                         # 4
        {EMAIL: email, PASSWORD: password, NAME: None},                     # 5

        # all fields is empty 
        {},

        # without one field
        {PASSWORD: password, NAME: name},                                   # 6
        {EMAIL: email, NAME: name},                                         # 7
        {EMAIL: email, PASSWORD: password}                                  # 8
    ]

    payload_wrong_credentials = [
        # пробел в логине
        {EMAIL : " ", PASSWORD : password},                                 # 0
        {EMAIL : " " + email, PASSWORD : password},                         # 1 fail - checked
        {EMAIL : email[:5] + " "+ email[5:], PASSWORD : password},          # 2
        {EMAIL : email + " ", PASSWORD : password},                         # 3 fail - checked
        
        # пробел в пароле
        {EMAIL : email, PASSWORD : " "},                                    # 4
        {EMAIL : email, PASSWORD : " " + password},                         # 5
        {EMAIL : email, PASSWORD : password[:5] + ' ' + password[5:]},      # 6
        {EMAIL : email, PASSWORD : password + " "},                         # 7
        
        # число символов валидного логина, отличное от len(email)
        {EMAIL : email[0], PASSWORD : password},                            # 8
        {EMAIL : email[:2], PASSWORD : password},                           # 9
        {EMAIL : email[:9], PASSWORD : password},                           # 10
        {EMAIL : email + email[0], PASSWORD : password},                    # 11
        {EMAIL : email + email[0:2], PASSWORD : password},                  # 12
        {EMAIL : email + email[0:5], PASSWORD : password},                  # 13
        {EMAIL : email*2, PASSWORD : password},                             # 14
        
        # email без необходимых символов или с неверными символами
        # используя функцию replace
        # без .
        {EMAIL : post_name + domen.replace('.', '') , PASSWORD : password},         # 15
        # без @
        {EMAIL : post_name + domen.replace('@', '') , PASSWORD : password},         # 16
        # без ru
        {EMAIL : post_name + domen.replace('ru', '') , PASSWORD : password},        # 17
        # без yandex
        {EMAIL : post_name + domen.replace('yandex', '') , PASSWORD : password},    # 18
        # только domen
        {EMAIL : post_name + domen.replace('yandex', '') , PASSWORD : password},    # 19
        # только собака post_name + '@'
        {EMAIL : post_name + domen.replace('yandex', '') , PASSWORD : password},    # 20

        # слишком короткое имя почты с валидным доменом
        {EMAIL : post_name [0] + domen , PASSWORD : password},                      # 21
        {EMAIL : post_name [:2] + domen , PASSWORD : password},                     # 22
        {EMAIL : post_name [:5] + domen , PASSWORD : password},                     # 23
        {EMAIL : post_name [:len(post_name)-2] + domen , PASSWORD : password},      # 24
        {EMAIL : post_name [:len(post_name)-1] + domen , PASSWORD : password},      # 25

        
        # число символов валидного пароля, отличное от len(password)
        {EMAIL : email, PASSWORD : password[0]},                            # 26
        {EMAIL : email, PASSWORD : password[:2]},                           # 27
        {EMAIL : email, PASSWORD : password[:4]},                           # 28
        {EMAIL : email, PASSWORD : password[:6]},                           # 29 
        {EMAIL : email, PASSWORD : password[:7]},                           # 30
        {EMAIL : email, PASSWORD : password + password[0]},                 # 31
        {EMAIL : email, PASSWORD : password + password[0:2]},               # 32
        {EMAIL : email, PASSWORD : password + password[0:5]},               # 33
        {EMAIL : email, PASSWORD : password*2},                             # 34
        
        # логин / пароль с валидными символами, но нарушенной последовательностью
        {EMAIL : email[::-1], PASSWORD : password},                         # 35
        {EMAIL : email, PASSWORD : password[::-1]},                         # 36
        
        # логин / пароль CAPS'ом
        {EMAIL : email.upper(), PASSWORD : password},                       # 37 fail
        {EMAIL : email, PASSWORD : password.upper()}                        # 38
    ]


class StatusCodes:
    # статус-коды
    OK              = 200
    CREATED         = 201
    ACCEPTED        = 202
    BAD_REQUEST     = 400
    UNAUTHORIZED    = 401
    FORBIDDEN       = 403
    NOT_FOUND       = 404
    CONFLICT        = 409
    INT_SERV_ERR    = 500          

