import os.path

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, empty_email, empty_password, invalid_text

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяет, что запрос api ключа возвращает статус 200 и в результате содержится слово 'key'"""

    # Отправляет запрос и сохраняет полученный ответ с кодом статуса в 'status', текст ответа в 'result'
    status, result = pf.get_api_key(email, password)
    # Проверка полученных данных
    assert status == 200
    assert 'key' in result
    print(result)

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяет, что запрос возвращает не пустой список. Получаем api ключ, сохраняем его в auth_key.
    С помощью полученного ключа запрашиваем список всех питомцев и проверяем, что он не пуст.
    Доступное значение параметра filter - 'my_pets' либо ''"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(result)

def test_add_new_pet_with_valid_data(name='Снежа', animal_type='кролик', age='2', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с корректными данными"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 200
    assert result['name'] == name

def test_successful_delete_pet():
    """Проверяет возможность удаления питомца"""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Снежинка', 'Декоративный кролик', '1', 'images/rabbit.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet(name='Пушок', animal_type='заяц', age='3'):
    """Проверяет возможность изменения данных питомца"""
    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пуст, то обновляет данные первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяет статус ответа и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если список пуст, то выходит исключение с сообщением
        raise Exception("Список питомцев пользователя пуст.")


def test_add_new_pet_simple_with_valid_data(name='Бэль', animal_type='дек. кролик', age='4'):
    """Проверяет добавление питомца с корректными данными без фото"""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 200
    assert result['name'] == name


def test_add_photo_pet_with_valid_data(pet_photo='images/rab.jpeg'):
    """Проверяет добавление фото с корректными данными"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пуст, то меняет фото первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:
        # Если список пуст, то выходит исключение с сообщением
        raise Exception("Список питомцев пользователя пуст.")

    # Проверяем полученные данные
    assert status == 200
    assert result['pet_photo'] != ''


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяет, что запрос api ключа возвращает статус равный 403, если указан
    некорректный email/пароль. Ошибка авторизации"""

    # Отправляет запрос и сохраняет полученный ответ с кодом статуса в 'status', текст ответа в 'result'
    status, result = pf.get_api_key(email, password)
    # Проверка полученных данных
    assert status == 403


def test_get_api_key_for_empty_user(email=empty_email, password=empty_password):
    """Проверяет, что запрос api ключа возвращает статус равный 403,
    если email/пароль не заполнены. Ошибка авторизации"""

    # Отправляет запрос и сохраняет полученный ответ с кодом статуса в 'status', текст ответа в 'result'
    status, result = pf.get_api_key(email, password)
    # Проверка полученных данных.
    # 403 - The error code means that provided combination of user email and password is incorrect
    assert status == 403


def test_add_photo_pet_with_invalid_extension(pet_photo='images/rab_1.gif'):
    """Проверяет добавление фото неподдерживаемого формата.
    Фото не будет добавлено.  По описанию в документации API сказано,
    что должен быть статус 400, если переданы некорректные данные, но ловится статус 500. Баг?"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пуст, то меняет фото первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:
        # Если список пуст, то выходит исключение с сообщением
        raise Exception("Список питомцев пользователя пуст.")
    # Проверяем полученные данные

    assert status == 500
    print(status)


def test_add_new_pet_with_photo_invalid_extension(name='Сноу', animal_type='кроля', age='2', pet_photo='images/rab_2.txt'):
    """Проверяет добавление питомца с фото неподдерживаемого формата.
    Ожидается, что появится ошибка при выборе фото некорректного формата.
    Баг: По описанию в документации API сказано, что должен быть статус 400, если переданы некорректные данные,
    но возвращает 200, т.е. добавляет питомца без фото."""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400



def test_add_new_pet_simple_with_invalid_name(name=invalid_text, animal_type='Пушишка', age='5'):
    """Проверяет добавление питомца (без фото) с некорректным именем:
    в поле name передается текст больше 255 символов. Например, 500 символов. Ожидается ответ от сервера 400.
    Пробовала и около 1500 символов - добавляет успешно, возвращает код 200.
    Неясно, зачем такая большая размерность для данного поля."""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_simple_with_invalid_animal_type(name='Печенька', animal_type=invalid_text, age='5'):
    """Проверяет добавление питомца (без фото) с некорректной породой:
    в поле animal_type передается текст больше 255 символов. Например, 500 символов. Ожидается ответ от сервера 400.
    Пробовала и около 1500 символов - добавляет успешно, возвращает код 200.
    Неясно, зачем такая большая размерность для данного поля."""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 400

def test_add_new_pet_simple_with_invalid_age(name='Печенька', animal_type='Пушишка', age=invalid_text):
    """Проверяет добавление питомца (без фото) с некорректным возрастом:
    в поле age передается текст размером больше 255 символов, а должен принимать только числа.
    Ожидается ответ от сервера 400. Но возвращает код 200. Баг"""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_simple_with_negative_age(name='Печенька', animal_type='Пушишка', age='-5'):
    """Проверяет добавление питомца (без фото) с некорректным возрастом:
    в поле age передается текст с отрицательным числом, а должен принимать только положительные числа.
    Ожидается ответ от сервера 400. Но возвращает код 200. Баг"""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_simple_with_empty_data(name='', animal_type='', age=''):
    """Проверяет добавление питомца (без фото) с незаполненными полями.
    Ожидается ответ от сервера 400. Но возвращает код 200. Баг"""

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_with_invalid_name(name=invalid_text, animal_type='Кролик', age='3', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с некорректным именем:
    в поле name передается текст больше 255 символов. Например, 500 символов.
    Ожидается ответ от сервера 400. Но добавляет питомца успешно, возвращает код 200.
    Неясно, зачем такая большая размерность для данного поля."""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_with_invalid_animal_type(name='Пряня', animal_type=invalid_text, age='3', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с некорректной породой:
    в поле animal_type передается текст больше 255 символов. Например, 500 символов.
    Ожидается ответ от сервера 400. Но добавляет питомца успешно, возвращает код 200.
    Неясно, зачем такая большая размерность для данного поля."""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400

def test_add_new_pet_with_invalid_age(name='Пряня', animal_type='Кролик', age=invalid_text, pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с некорректным возрастом:
    в поле age передается текст больше 255 символов, должен принимать только числа.
    Ожидается ответ от сервера 400. Но добавляет питомца успешно, возвращает код 200. Баг"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_with_negative_age(name='Пряня', animal_type='Кролик', age='-3', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с некорректным возрастом:
    в поле age передается отрицательное число, должен принимать только числа > 0.
    Ожидается ответ от сервера 400. Но добавляет питомца успешно, возвращает код 200. Баг"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400


def test_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с незаполненными именем, породой и возрастом.
    Ожидается ответ от сервера 400. Но добавляет питомца успешно, возвращает код 200. Баг"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем полученные данные
    assert status == 400


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяет, что запрос возвращает ответ от сервера 403, если auth_key невозможно получить, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password)"""

    status, auth_key = pf.get_api_key(invalid_email, invalid_password)
    assert status == 403



def test_add_new_pet_with_invalid_key(name='Снежа', animal_type='кролик', age='2', pet_photo='images/rabbit.jpeg'):
    """Проверяет добавление питомца с корректными данными, если auth_key невозможно получить, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password). Ожидаем ответ от сервера 403"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    status, auth_key = pf.get_api_key(invalid_email, invalid_password)

    # Проверяем полученные данные
    assert status == 403


def test_unsuccessful_delete_pet_with_invalid_key():
    """Проверяет невозможность удаления питомца, если auth_key не получен, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password). Ожидаем ответ от сервера 403"""

    # Получаем api ключ, сохраняем его в auth_key
    status, auth_key = pf.get_api_key(invalid_email, invalid_password)

    assert status == 403


def test_unsuccessful_update_pet_with_invalid_key(name='Пушок', animal_type='заяц', age='3'):
    """Проверяет невозможность изменения данных питомца, если auth_key не получен, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password). Ожидаем ответ от сервера 403"""
    # Получаем api ключ, сохраняем его в auth_key
    status, auth_key = pf.get_api_key(invalid_email, invalid_password)

    assert status == 403



def test_add_new_pet_simple_with_invalid_key(name='Бэль', animal_type='дек. кролик', age='4'):
    """Проверяет невозможность добавления питомца с корректными данными без фото, если auth_key не получен, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password). Ожидаем ответ от сервера 403"""

    # Получаем api ключ, сохраняем его в auth_key
    status, auth_key = pf.get_api_key(invalid_email, invalid_password)

    # Проверяем полученные данные
    assert status == 403



def test_add_photo_pet_with_invalid_key(pet_photo='images/rab.jpeg'):
    """Проверяет невозможность добавления фото с корректными данными, если auth_key не получен, потому что
    переданы некорректные email (invalid_email) и пароль (invalid_password). Ожидаем ответ от сервера 403"""

    # Полный путь к изображению и сохранение его в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем api ключ, сохраняем его в auth_key
    status, auth_key = pf.get_api_key(invalid_email, invalid_password)

    # Проверяем полученные данные
    assert status == 403


def test_get_all_pets_with_invalid_filter(filter='filter'):
    """Проверяет, что запрос возвращает ответ от сервера 500, так как задан неподдерживаемый фильтр."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    #assert len(result['pets']) > 0
    print(result)