import json

import requests


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденным по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url+'/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может
        иметь либо пустое значение - получить список всех питомцев либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет данные о новом добавляемом питомце на сервер и возвращает статус запроса и результат в формате
        JSON с данными добавленного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url+'/api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет запрос на сервер на удаление питомца по pet_id и возвращает
        статус запроса и результат в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'/api/pets/'+pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер запрос на обновление/изменение данных питомца по pet_id и возвращает
        статус запроса и результат в формате JSON"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url+'/api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет данные о новом добавляемом питомце без фото на сервер и возвращает статус запроса и результат в формате
        JSON с данными добавленного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url+'/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер запрос на добавление фото питомца по pet_id и возвращает
        статус запроса и результат в формате JSON"""

        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url+'/api/pets/set_photo/'+pet_id, headers=headers, files=file)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


