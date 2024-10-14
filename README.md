# Bulletin_board_backend
__1. До начала разворачивания проекта, на PC должны быть установлены следующие приложения:__
##
        Python 3.12
        Redis 5
__2. Скопировать из репозитория develop__
##
        git clone https://github.com/salfa-ru/Bulletin_board_backend.git
__Если спрашивает имя, пароль, то попробуйте сначала склонировать по-другому:__
##
        git clone git@github.com:salfa-ru/Bulletin_board_backend.git
__3. Необходимо создать .env  файл с переменными окружения в корне проекта.__
##
        (образец переменных лежит в файле .env.dev)
__4. Запуск базы postgresql под именем postgres__
##
        psql -U postgres
- Создаем базу bulletin и присоединяемся к ней
##
        create database bulletin;\c bulletin
- Преобразуем базу Postgres в Postgis
## 
        CREATE EXTENSION postgis;
- выход из postgresql ctr+c

__5. Устанавливаем зависимости__
##
        pip install -r requirements.txt

__6. Создаём 2 директории для корректного функционирования Gdal__
##
        export CPLUS_INCLUDE_PATH=/usr/include/gdal
        export C_INCLUDE_PATH=/usr/include/gdal

__7. Запускаем миграции__
##
        python manage.py makemigrations
##
        python manage.py migrate

__8. Запуск проекта__
##
      python manage.py runserver

__9. Загрузка тестовых данных__ (это получается не актуально можно удалять?)
##
      python manage.py loaddata filling_test_data

__10. Команда для запуска Celery (запускается и worker, и beat)__
##
      celery -A config worker --loglevel=info -S django -B

__11. Команда для просмотра логов Celery beat, видно какие задачи видит и какое расписание__
##
      celery -A config beat --loglevel=DEBUG

sign_in_email:
1. Авторизованный пользователь -> В ответе статус 400 и сообщение о том, что уже авторизован.
2. Неавторизованный пользователь в первый раз (без email в БД) -> В ответе статус 201. В сессии ключ "email". Создаем в БД пользователя. Отправляем код на почту.
3. Неавторизованный пользователь в очередной раз (с email в БД) -> В ответе статус 200. В сессии ключ "email". Отправляем код на почту.
4. Забаненный пользователь -> В ответе код 403, оставшееся время бана "ban_time" и сообщение о том, что пользователь забанен.


confirm_code:
1. Авторизованный пользователь -> В ответе статус 400 и сообщение о том, что уже авторизован.
2. Неавторизованный пользователь без email в БД -> В ответе статус 404 и сообщение о том, что пользователь не найден.
3. Неавторизованный пользователь без одноразового кода в БД -> В ответе статус 404 и сообщение о том, что код не найден.
4. Забаненный пользователь -> В ответе код 403, время до снятия бана "ban_time" и сообщение о том, что пользователь забанен.
5. Пользователь ввел код с истекшим сроком годности, количество повторных отправок кода меньше допустимого значения -> В ответе код 400 и сообщение о том, что время ожидания истекло. Повторная отправка кода на email.
6. Пользователь ввел код с истекшим сроком годности, количество повторных отправок кода больше допустимого значения -> В ответе код 403 и сообщение о том, что слишком много запросов на отправку кода и пользователь забанен на 24 часа. Бан пользователя.
7. Пользователь ввел правильный код, пользователь зашел в первый раз -> В ответе статус 200 и поля id, email пользователя. Сброс всех попыток. 
8. Пользователь ввел правильный код, пользователь зашел в очередной раз -> В ответе статус 200 и поля id, email пользователя. Сброс всех попыток. Логиним пользователя.
9. Пользователь ввел неправильный код, количество попыток ввода кода меньше допустимого значения -> В ответе статус 400, количество оставшихся попыток ввода кода "remaining_attempts" и сообщение о том, что пользователь неправильно ввел код (количество раз).
10. Пользователь ввел неправильный код, количество попыток ввода кода больше допустимого значения -> В ответе статус 403, количество оставшихся попыток ввода кода "remaining_attempts" и сообщение о том, что пользователь неправильно ввел код (количество раз) и пользователь забанен на 24 часа. Бан пользователя.


sign_up_profile:
1. Авторизованный пользователь -> В ответе статус 400 и сообщение о том, что уже авторизован.
2. Неавторизованный пользователь без email в БД -> В ответе статус 404 и сообщение о том, что пользователь не найден.
3. Забаненный пользователь -> В ответе код 403, оставшееся время бана "ban_time" и сообщение о том, что пользователь забанен.
4. Пользователь ввел валидные данные -> В ответе статус 200 и поля id, name, phone_number пользователя. Создаем в БД профиль с номером телефона и именем. Логиним пользователя.

- python manage.py update_translation_fields

celery -A config worker -l info
celery -A config beat -l INFO

https://crusat.ru/blog/105-kak-proshe-vsego-razvernut-django-proekt-cherez-do/
https://yandex.ru/video/preview/63361828915957190
<!-- docker compose -f docker-compose_celery_images.yaml up -->
<!-- CTRL-p CTRL-q  exit fm container -->
<!-- docker exec -it 9bfbb562767a /bin/bash изпод контейнера -->
<!-- gunicorn config.wsgi:application --bind 0.0.0.0:8000 -->
<!-- https://dzen.ru/video/watch/660cfbb2aca2404a9108e66c -->
<!-- python manage.py loaddata --exclude contenttypes db1.json -->

<!-- python manage.py create_super_user2
python manage.py create_users
python manage.py create_profile
python manage.py create_category
python manage.py create_persanal_items
python manage.py create_auto
python manage.py create_favorite
python manage.py create_images
python manage.py create_promotions
python manage.py create_like -->
<!-- map/templates/map/home_map.html: -->
  <!-- <script src="http://90.156.226.147:8000/static/map.js" ></script>
 <link  src="http://90.156.226.147:8000/static/map.css" >
  <link  src="http://90.156.226.147:8000/static/map.js" >
  <link  src="{%'http://90.156.226.147:8000/static/map.js' %}" > -->
<!-- apt install -y netcat
nc -vz 0.0.0.0 8000
  apt install net-tools
  netstat -ntlp -->
  <!-- fuser -k -n tcp 3000 -->
  <!-- apt-get install psmisc -->
  <!-- && python manage.py -y collectstatic & -->
