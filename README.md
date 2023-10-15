# praktikum_new_diplom

![](https://github.com/LenarFazlyev/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## О проекте

Социальная сеть для любителей готовить.
Здесь вы можете публиковать рецепты, подписываться на других пользователей и добавлять рецепты в Избранное.А также есть возможность скачать список покупок добавленных в карзину рецепта/ов. Возможно появится фича для заказа продуктов в одном из сервисов для доставки.

[Ссылка на страницу рецептов](https://foodsite-lenarf.sytes.net/recipes)

[Ссылка на файл с документацией](https://github.com/LenarFazlyev/foodgram-project-react/blob/master/docs/openapi-schema.yml)

[https://foodsite-lenarf.sytes.net/api/docs/](https://foodsite-lenarf.sytes.net/api/docs/)


## Стек технологий

- Python
- Django
- djangorestframework
- Nginx
- gunicorn
- Docker
- GitHub Action
- PostgreSQL

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/<Ваше Имя>/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

P.S. В директории foodgram-project-react/infra необходимо создать файл .env и прописать необходимые значения переменных. Смотри пример ниже и в файле .env.example
```
SECRET_KEY = '<Ваш Ключ>'
```

## Как развернуть проект на сервере
Создаем папку foodgram
```
cd ~
mkdir foodgram
```
В ней создаем файл .env. Пример содержимого в .env.example
```
nano foodgram/.env
```
Настриваем "внешний" nginx. См. пример в default.example
```
sudo nano /etc/nginx/sites-available/default
```
Получаем HTTPS-сертификат:
```
sudo certbot --nginx
```
Не забываем добавлять секреты в GitHub actions:

- DOCKER_USERNAME - логин от Docker Hub
- DOCKER_PASSWORD - пароль от Docker Hub
- SSH_KEY - закрытый ssh-ключ для подключения к серверу
- SSH_PASSPHRASE - passphrase от этого ключа
- USER - имя пользователя на сервере
- HOST - IP-адрес сервера
- TELEGRAM_TO - ID телеграм-аккаунта для оповещения об успешном деплое
- TELEGRAM_TOKEN - токен телеграм-бота



## Автор:
 :grinning: Lenar :sunglasses::boom: