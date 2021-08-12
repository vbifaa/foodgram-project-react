from typing import Dict, Any, List


class Data:
    tags = [
        {
            'name': 'Завтрак',
            'color': '#48D1CC',
            'slug': 'breakfast'
        },
        {
            'name': 'Обед',
            'color': '#00BFFF',
            'slug': 'lunch'
        },
        {
            'name': 'Суп',
            'color': '#FFFF00',
            'slug': 'soup'
        },
        {
            'name': 'Ближневосточная кухня',
            'color': '#DC143C',
            'slug': 'middle-eastern-cuisine'
        }
    ]
    ingredients = [
        {
            'name': 'Свекла',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Лук',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Капуста',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Помидоры',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Соль',
            'measurement_unit': 'г'
        },
        {
            'name': 'Перец',
            'measurement_unit': 'г'
        },
        {
            'name': 'Мясо',
            'measurement_unit': 'г'
        },
        {
            'name': 'Яйцо',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Сало',
            'measurement_unit': 'г'
        },
        {
            'name': 'Лаваш',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Огурцы',
            'measurement_unit': 'шт'
        },
        {
            'name': 'Мокровь',
            'measurement_unit': 'г'
        },
    ]
    users: List[Dict[str, Any]] = [
        {
            'email': 'vpupkin@yandex.ru',
            'username': 'vasya.pupkin',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'augashasocmscodvoddsivu'
        },
        {
            'email': 'voltvordol@yandex.ru',
            'username': 'vvoltvordol',
            'first_name': 'Володя',
            'last_name': 'Твёрдолобов',
            'password': 'augashasocmcdmcalllw1'
        }
    ]