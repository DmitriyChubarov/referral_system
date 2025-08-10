# referral_system
# Реализация веб-приложения c простой реферальной системой


## Возможности интерфейса
- Авторизация по номеру телефона с помощью 4-го кода
- Просмотр профиля пользователя
- Ввод реферального кода другого пользователя

## Возможности API:
- http://127.0.0.1:8000/auth/auth_code/ - отправка номера телефона и получение кода для авторизации, к запросу необходимо прикрепить phone_number.
Возвращает 4-ый код (или статус ошибки).
- http://127.0.0.1:8000/auth/auth/login/ - отправка полученного кода для авторизации, к запросу необходимо прикрепить phone_number и code.
Возвращает токен аутентификации, твой реферальный код и статус создания аккаунта (или статус ошибки).
- http://127.0.0.1:8000/auth/auth/profile/ - получение данных о профиле, к запросу необходимо прикрепить Token в Headers.
Возвращает токен аутентификации, твой реферальный код, поле ввода чужого реферального кода и список людей, которые использовали твой реферальный код (или статус ошибки).
- http://127.0.0.1:8000/auth/auth/invited_code/ - ввод чужого реферального кода, к запросу необходимо прикрепить Token в Headers и invited_code.
Возвращает статус ввода.

## Приложение было опубликовано на pythonanywhere по ссылке - https://dmitriychubarov.pythonanywhere.com/auth/auth_code_html/
Так как на pythonanywhere БД PostgreSQL доступна только в платной подписке, я переделал версию на сайте на MySQL. Postman коллекцию для теста этой версии можно взять тут - 
https://disk.yandex.ru/d/aqVD-apl8txjyw. Поля phone_number, code, invited_code и Token соотвественно нужно менять в процессе тестирования.

### Технологии

- Python
- Django
- Django REST framework
- PostgreSQL

### Подготовка БД перед запуском

Создаём БД и пользователя для работы сервиса, выдаём новому пользователю права на БД:
```bash
psql postgres
```
```sql
CREATE DATABASE ref_sys;
CREATE USER ref_sys WITH PASSWORD 'ref_sys';
GRANT ALL PRIVILEGES ON DATABASE ref_sys to ref_sys;
\q
```

### Установка на MacOS/Linux

Открываем терминал, создаём папку, в которой будет располагаться проект и переходим в неё:
```bash
mkdir /ваш/путь
cd /ваш/путь
```
Клонируем репозотирий в эту папку:
```bash 
git clone https://github.com/DmitriyChubarov/referral_system.git
```
После чего создаём новое виртуальное окружение. Запускаем и устанавливаем в него django, DRF и все необходимое:
```bash
pipenv shell
pip install django
pip install djangorestframework
pip install psycopg2-binary
pip install requests

```
Окончательно настраиваем проект:
```bash
cd referral_system/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
  
### Контакты
- tg: @eeezz_z
- gh: https://github.com/DmitriyChubarov
