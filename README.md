# Проектная работа 6 и 7 спринтов
Задачи по обоим спринтам можно посмотреть в /tasks

## Ссылка на репозиторий с проектом:
https://github.com/AlexanderNkn/Auth_sprint_2

## Описание
Это API для аутентификации пользователей

## Установка
- склонируйте проект с реппозитория GitHub
    ```
    git clone https://github.com/AlexanderNkn/Auth_sprint_2.git
    ```
- соберите образ
    ```
    docker-compose build --no-cache
    ```
- запустите проект
    ```
    docker-compose up -d
    ```

## Тестирование
### В контейнере
- тесты запускаются автоматически при старте контейнера. Для перезапуска выполните
    ```
    docker-compose start test_auth
    ```

### Дополнительные возможности
- просмотр логов
    ```
    docker-compose logs -f
    ```
- очистка базы данных из консоли
    ```
    flask recreate-database
    ```
- создание суперпользователя из консоли
    ```
    flask create-superuser name password
    ```

## Использование
### Документация доступна по адресу
-    http://localhost/api/openapi

### Примеры запросов
- логин пользователя
    ```
    /api/v1/auth/login
    ```
    ```
    curl -X POST "http://localhost/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"password\":12345,\"username\":\"yandex\"}"

    401	Error: Unauthorized

    {
      "message": "user is not exist",
      "status": "error"
    }
    ```
- изменить роль пользователя
    ```
    /api/v1/role/<uuid:user_id>
    ```
    ```
    curl -X PATCH "http://localhost/api/v1/role/<uuid:role_id>" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"code\":\"admin\",\"description\":\"unlimited access to all actions\"}"

    200	info about role was changed successfully

    Media type
    
    application/json
    Controls Accept header.
    Example Value
    Schema
    {
      "message": "info about role was changed successfully",
      "role": {
        "code": "admin",
        "description": "unlimited access to all actions",
        "id": "a9c6e8da-f2bf-458a-978b-d2f50a031451"
      },
      "status": "success"
    }
    ```
