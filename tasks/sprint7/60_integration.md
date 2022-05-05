### Интеграция сервиса Auth с другими сервисами

Подготовьте Auth сервис к интеграции с другими сервисами вашего сайта. Сгенерируйте схему взаимодействия с Auth сервисом в формате, который используется в вашем сервисе.
Создайте интеграцию Auth-сервиса и AsyncAPI-сервиса, используя контракт, который вы сгенерировали в прошлом задании.
При создании интеграции не забудьте учесть изящную деградацию Auth-сервиса. Как вы уже выяснили ранее, Auth сервис один из самых нагруженных, потому что в него ходят большинство сервисов сайта. И если он откажет, сайт отказать не должен. Обязательно учтите этот сценарий в интеграциях с Auth-сервисом.

Подзадачи:
 - запустить отдельный сервер с документацией и шаблонами моделей и эндпойнтов. Сервер автоматически генерируется с помощью openapi-codegen
 - исправить остановку nginx при падении любого upstream
 - в качестве изящной деградации высылать пользователю сообщение с номером задачи в sentry
 - для ограничения нагрузки на сервер во время восстановления после сбоя применить Circuit Breaker
 - смержить сервис Async_api_2
 - добавить на эндпойнты Async_api_2 декоратор для проверки разрешений пользователя. При этом из Async_api_2 должны высылаться запросы в Auth