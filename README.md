Интерфейс для тестирования API

https://aberq.pythonanywhere.com



Развертка проекта

Я сделал базу данных пользуясь СУБД PostgreSQL и Docker-контейнер, поэтому вы можете ввести "docker-compose up --build" в терминал для быстрой развертки проекта.

ВНИМАНИЕ!!!

Если вы планируете пользоваться приложение через стандартный тестовый сервер django('python manage.py runserver'), то необходимо переключить хоста в базе данных с 'db' на 'localhost'
в settings.py. Я оставил там вспомогательный комментарий(93 строка)


Документация API


Также есть APi-документация на Swagger http://127.0.0.1:8000/swagger (На pythonanywhere не показывает)


1. Создать пользователя или получить код подтверждения

Эндпоинт: https://aberq.pythonanywhere.com/api/get-or-create-user/

Метод: POST

Описание: Создаёт нового пользователя по номеру телефона или возвращает код подтверждения (auth_code) для уже существующего пользователя.

Тело запроса:

phone_number: Номер телефона пользователя.

Ответы:

200 OK: Пользователь существует, возвращается auth_code.

Пример: {"auth_code": "string"}

201 Created: Пользователь был создан, возвращается auth_code.

Пример: {"auth_code": "string"}

400 Bad Request: Ошибка в запросе (например, если не передан номер телефона).

Пример: {"error": "Phone number is required"}

2.Аутентификация пользователя

Эндпоинт: https://aberq.pythonanywhere.com/api/autorize/

Метод: POST

Описание: Аутентифицирует пользователя по коду подтверждения (auth_code) и генерирует JWT токен.

Тело запроса:

auth_code: Код подтверждения для аутентификации.

Ответы:

200 OK: Токен успешно сгенерирован.

Пример: {"token": "string"}

400 Bad Request: Некорректный код подтверждения.

Пример: {"error": "Invalid auth code"}

3. Профиль пользователя
Эндпоинт: https://aberq.pythonanywhere.com/api/profile/

Метод: GET

Описание: Возвращает информацию о текущем профиле пользователя, включая данные о его рефералах. Требуется аутентификация с JWT токеном.

Ответ:

200 OK: Данные профиля пользователя.

Пример:


{
  "id": "integer",
  
  "phone_number": "string",
  
  "referral_code": "string",
  
  "referred_by": "string",  // Реферал (если есть)
  
  "referrals": ["string"]   // Список рефералов (если есть)
  
}


4. Применение реферального кода

Эндпоинт: https://aberq.pythonanywhere.com/api/input_referral_code/

Метод: POST

Описание: Позволяет пользователю ввести реферальный код другого пользователя.

Тело запроса:

referral_code: Реферальный код.

Ответы:

200 OK: Реферальный код успешно применен.

Пример: {"detail": "Referral code applied successfully."}

400 Bad Request: Ошибка в запросе (например, реферальный код не передан).

Пример: {"detail": "Referral code is required."}

404 Not Found: Реферальный код не найден.

Пример: {"detail": "User with this referral code not found."}

403 Forbidden: Запрещено использовать свой собственный реферальный код.

Пример: {"detail": "You cannot use your own referral code."}
