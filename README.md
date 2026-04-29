# Blog Platform API

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-DRF-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

## Описание проекта

REST API для блог-платформы.

Цель проекта:

Система должна позволять пользователям:
- авторизовываться через Oauth
- создавать записи (посты)
- просматривать записи других пользователей
- ставить лайки
- фильтровать и сортировать записи

Функциональность:

- Авторизация через GitHun OAuth;
- просмотр/создание/редактирование/удаление постов/поста;
- Права доступа;
- Лайк поставо;
- Фильтрация постав;
- Сортировка постов;
- Swagger.

## Технологии

- Python 3.12в
- Django
- Django REST Framework
- PostgreSQL
- django-filter
- drf-spectacular
- django-allauth
- dj-rest-auth
- Docker
- Docker Compose
- Gunicorn
- Nginx

## Установка и запуск

Создайте файл `.env` в корне проекта на основе `.env.example`.

Запуск через Docker Compose:

```bash
sudo docker-compose up --build -d
```

Создать суперпользователя:
```bash
sudo docker-compose exec web python3 manage.py createsuperuser
```

Запуск тестов:
```bash
sudo docker-compose exec web python3 manage.py test
```

## Swagger
```bash
http://127.0.0.1/api/docs/
```


## Автор
:trollface: Валентин :sunglasses:  