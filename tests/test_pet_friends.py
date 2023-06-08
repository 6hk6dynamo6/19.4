from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
import uuid

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key in result'
    print(result)


def test_get_list_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(auth_key)
    print(result)

def test_add_new_pet_with_valid_data(name='Пончик', animal_type='бродяжка',
                                     age="4", pet_photo='images/kotenok-sidit18-1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Nonamedog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    print(result)

def test_successful_update_self_pet_info(name='Пончик', animal_type='бродяжка', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

###########HOMEWORK#######################################################################

def test_add_new_pet_without_photo_valid_data(name='Пончик', animal_type='бродяжка',
                                     age='4'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.Add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_to_pet(pet_photo='images/Nonamedog.jpg'):
    """Проверяем что можно добавить фото к ранее загруженному питомцу"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Nonamedog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ''
    print(status, result)
####
#1
def test_get_api_key_for_invalid_email_user(email = invalid_email, password = valid_password):
    """ Негативный тест. Проверяем что запрос api ключа возвращает статус 403 когда введен некорректный email"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
#2
def test_get_api_key_for_invalid_password_user(email = invalid_email, password = invalid_password):
    """ Негативный тест. Проверяем что запрос api ключа возвращает статус 403 когда введен некорректный password """
    status, result = pf.get_api_key(email, password)
    assert status == 403
#3
def test_get_list_pets_with_valid_key_invalid_filter(filter=5):
    """ Негативный тест. Некорректное значение filter, значение int
    Проверяем что запрос всех питомцев НЕ возвращает ответ при некорректном значении filter.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев.
    Указываем значение параметра filter с типом int"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500

#4 Bug
def test_add_new_pet_with_invalid_data(name='', animal_type='',
                                      age= '', pet_photo='images/kotenok-sidit18-1.jpg'):
    """Негативный тест.Проверяем что нельзя добавить питомца с некорректными данными.
    Пустые атрибуты name, animal_type, age пустые"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


#5 Bug
def test_add_new_pet_with_invalid_data_with_spaces(name=' ', animal_type=' ',
                                      age=' ', pet_photo='images/kotenok-sidit18-1.jpg'):
    """Негативный тест. Проверяем что нельзя добавить питомца с некорректными данными.
    Пробелы в атрибутах name, animal_type, age """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
#6 Bug
def test_add_new_pet_with_invalid_format_of_photo_data(name='Пончик', animal_type='бродяжка',
                                     age='4', pet_photo='images/Krokodil.txt'):
    """Негативный тест. Проверяем что нельзя добавить питомца с некорректными данными. Формат файла txt."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

#7
def test_add_photo_to_pet_invalid(pet_photo='images/Krokodil.txt'):
    """Негативный кейс. Проверяем что нельзя файл txt загрузить к ранее загруженному питомцу"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Nonamedog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 500

#8
def test_unsuccessful_update_self_pet_info(name='Лёнчик', animal_type='бродяжка', age='4'):
    """Негативный тест. Проверяем возможность обновления информации о питомце c несуществующими данными"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 404
        print(result)
#9  Bug
def test_unsuccessful_delete_self_pet_with_random_uuid():
    """Негативный тест. Проверяем отсутствие возможности удаления несуществующего питомца.
    Случайно сгенерированный pet_id """

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Генерируем случайный uuid
    pet_id = str(uuid.uuid4())
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 400
#10
def test_unsuccessful_delete_self_pet_with_empty_pet_id():
    """Негативный тест. Проверяем отсутствие возможности удаления питомца c некорректным pet_id (пустая строка)"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = ''
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 404

#11
def test_unsuccessful_update_self_pet_info_with_empty_atributes(name='', animal_type='', age=''):
    """Негативный кейс.
    Проверяем отсутствие возможности обновления информации о питомце с незаполненными атрибутами"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Nonamedog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 404
