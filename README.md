# Grocery Assistant
Продуктовы помощник. В нём можно:
    1) Выкладывать рецепты
    2) Подписываться на авторов
    3) Добавлять рецепты в список любимых
    4) Добавлять рецепты в список покупок и создавать список покупок на основе ингредиентов этих рецептов


### Подготовка к сборке:
1) Установите докер по ссылке https://www.docker.com/products/docker-desktop
2) Создайте файл  *.env* и заполните его аналогично *backend/grocery_assistant/example.env*


### Сборка:
1) Перейдите в терменале в директорию *infra* и выполните команду:
'docker-compose up'

2) Зайдите в контейнер backend, для этого:
    2.1) Введите 'docker ps' и найдите <CONTAINER ID> для которого NAMES=infra_backend_1 (главное, чтобы было слово backend)
    2.2) Введите 'docker exec -it <CONTAINER ID> bash' (где <CONTAINER ID> из предыдущего пункта)

3) Сделайте миграции, выполните последовательно команды:
'python manage.py migrate'

4) Создайте суперпользователя(админа):
'python manage.py createsuperuser'

5) Соберите статистику:
'python manage.py collectstatic'


### Проверка, что всё получилось:
1) Зайдите на страницу в браузере по адресу http://127.0.0.1/admin/, для сервера будет http://public_ip/admin/(например мой адрес http://130.193.34.157/admin) или доменное имя.
2) Добавьте ингредиенты и теги.
3) Зайдите на страницу в браузере по адресу http://127.0.0.1/ (аналог 1-ому пункту для сервера)
4) Зарегестрируйтесь, доавляйте рецепты и жмите пользуйтесь остальной функциональностью


### В проекте использовались: 
Django(3.1.7), djangorestframework(3.12.2), gunicorn(20.0.4), nginx(1.19.3), postgres(12.4) 
 
 
### Связь: 
По всем вопросам писать https://github.com/vbifaa 
Ник vbifaa 