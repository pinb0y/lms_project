# Домашка. Docker
Проект платформа для обучения завернута в Docker контейнер

#### Для запуска создайте в корне файл .env следующего вида:
```commandline
# настройки Джанго
SECRET_KEY=***

# настройки БД
POSTGRES_DB= Имя вашей БД
POSTGRES_USER= Имя пользователя
POSTGRES_PASSWORD= Пароль
POSTGRES_HOST=Хост для подключения

# настройки редис для Celery
CELERY_BROKER_URL= 
CELERY_RESULT_BACKEND=

```
Введите команду
```commandline
sudo docker compose up -d --build
```