# FOODGRAM


## Продуктовый помощник

Проект FOODGRAM был создан в помощь общительным любителям вкусно готовить. Он дает возможность просматривать кулинарные рецепты, публиковать свои рецепты, организовать систему подписок и сохранять понравившиеся рецепты в "Избранное". Для упрощения походов в магазин есть опция "Список покупок", которая подготавливает общий список покупок для сформированного списка рецептов. "Список покупок" может быть выгружен в виде файла в формате PDF. Используется система тегов для быстрого поиска рецептов. 

В приложении реализована система авторизации и аутентификации на базе токенов. 

Для приложения настроен CI/CD процесс. 
Реализованы следующие функции: 
* автоматический запуск теста на соответствие требованиям PEP8; 
* обновление образов на DockerHub; 
* автоматический деплой на "боевой" сервер при push-е в главную ветку master. 

## Техническая информация 

Стек технологий: Python 3, Django, DjangoRestFramework, Gunicorn, React, Docker, Nginx, Postgres. 

Веб-сервер: Nginx, Gunicorn 
Frontend фреймворк: React 
Backend фреймворк: Django 
API фреймворк: Django REST 
База данных: PostgreSQL 

## Копирование проекта на компьютер разработчика 

git@github.com:ppk202301/foodgram-project-react.git 

## Настройка Workflow CI/CD в github 

Для организации автоматического процесса CI/CD на стороне компьютера разработчика в папке .github\workflow подготовлен файл master.yml.
Команды из этого файла будут вызываться на выполнение runner github при каждом push в ветку master проекта. 

В разделе Actions secrets and variables настроек проекта на github должны быть указаны следющие secrets (параметры): 

DEBUG=False  - опция отладчика, должна быть всегда False для правильной работы ПО  
SECRET_KEY   - стандартный ключ, который создается при создании Django проекта  
ALLOWED_HOSTS  - список хостов/доменов, для которых дотсупен текущий проект  
                 &nbsp;&nbsp;&emsp; изменить IP-адрес сервера и/или добавить имя хоста  
                 &nbsp;&emsp; пример формата задания значений '127.0.0.1, localhost'  

POSTGRES_DB    - имя БД - foodgram (по умолчанию)  
POSTGRES_USER  - логин для подключения к БД - django_user (по умолчанию)  
POSTGRES_PASSWORD - пароль для подключения к БД - mysecretpassword (по умолчанию)  
DB_HOST=db        - имя сервера базы данных  
DB_PORT=5432      - порт для подключения к БД  

DOCKER_USERNAME   - имя пользователя в DockerHub  
DOCKER_PASSWORD   - пароль пользователя в DockerHub  
HOST              - ip_address сервера, на который будет выполнен deploy  
USER              - имя пользователя удаленного сервера  
SSH_KEY           - приватный ключ для доступа к удаленному серверу  
PASSPHRASE        - кодовая фраза приватный ключ для доступа к удаленному серверу  

## Подготовка удаленной Ubuntu машины для deploy проекта 

В домашнем каталоге пользователя, для которого должен быть установлен проект, должна быть создана папка ./foodgram/, а в нее скопирован файл   
docker-compose.production.yml из проекта в git.

Установить Docker(CE) и Docker Compose:
```bash 
apt install docker-ce docker-compose -y
``` 

Проверить, что  Docker работает можно командой: 
```bash 
systemctl status docker 
``` 

### Локальное развертывание проекта с использованием Docker (Ubuntu) 

В корневой папке проекта должен быть создан файл .env. Указанные в этом файле параметры используются для локального запуска контейнера базы данных при помощи docker composer. Файл должен быть построен на примере example_dot_env.txt. Значения параметров должны соответствовать значениям параметров, используемых в Django проекте для подключения backend к базе данных Postresql.  

Из каталога проекта нужно выполнить команду 
```bash
sudo docker-compose up -d 
```

## Первый запуск проекта на локальной Ubuntu машине

Для подключения к контейнеру нужно выполнить команду 
```bash
sudo docker exec -it foodgram-backend bash 
``` 

Подготовить статику backend 
```bash
python manage.py collectstatic 
``` 

Скопировать статику backend 
```bash
 cp -r /app/cookbook/collected_static/.  /static_backend/
``` 

Создать superuser 
```bash
python manage.py createsuperuser 
``` 

Импортировать с базу список ингредиентов 
```bash
python manage.py import_ingredients_data 
``` 

Зайти по адресу  
http://localhost/admin  
и сделать в разделе Tag набор тегов для маркировки рецептов  

## Первый запуск проекта на удаленной Ubuntu машине

Подключиться к удаленной машине, напрмиер, через Bitvise клиента.  

В Terminal набрать команду  
```bash
sudo docker exec -it foodgram-backend bash  
``` 

Создать superuser 
```bash
python manage.py createsuperuser 
``` 

Импортировать с базу список ингредиентов 
```bash
python manage.py import_ingredients_data 
``` 

Зайти по адресу  
http://site_name/admin  
и сделать в разделе Tag набор тегов для маркировки рецептов  

## Тестовый сайт с дипломным заданием

Адрес сайта: https://foodgram-pp.hopto.org/
Админ
name=adminuser
email=adminuser@ya.com
password=AZS012##$$asf!!!!!
