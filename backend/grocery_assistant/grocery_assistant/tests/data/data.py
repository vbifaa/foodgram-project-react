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
            'name': 'Морковь',
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
    recipes: List[Dict[str, Any]] = [
        {
            'ingredients': [
                {'id': 1, 'amount': 1},
                {'id': 2, 'amount': 2},
                {'id': 3, 'amount': 3},
                {'id': 4, 'amount': 5},
                {'id': 6, 'amount': 10},
                {'id': 8, 'amount': 4}
            ],
            'tags': [2, 3],
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
            'name': 'Борщ',
            'text': 'Готовить с любовью',
            'cooking_time': 20
        },
        {
            "ingredients": [
                {'id': 9,'amount': 80},
                {'id': 6,'amount': 10},
                {'id': 8,'amount': 3}
                ],
                'tags': [1],
                'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
                'name': 'Яичница',
                'text': 'Нужна сковорода.',
                'cooking_time': 5
            }
    ]
