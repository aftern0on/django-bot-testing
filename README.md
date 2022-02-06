# Развертывание
1. Скачиваем проект. Создаем новую папку, открываем в ней консоль, набираем:
```bash
git init
git remote add origin git@github.com:aftern0on/django-bot-testing.git
git branch -m main
git pull origin main
```
2. Копируем файл `.env.dist`, копию переименовываем в `.env`
3. Разворачиваем Docker:
```bash
docker-compose up -d --build
```
4. Регестрируем нового пользователя для доступа в админ-панель (необязательно, там можно создать новые экземпляры классов вручную):
```bash
docker-compose exec backend python3 manage.py createsuperuser
```
5. Запускаем тесты:
```bash
docker-compose exec backend python3 manage.py test
```

# Что посмотреть
Во-первых схему БД пользовательских моделей:
![alt text](https://github.com/aftern0on/django-bot-testing/blob/main/img/db_view.png)
* __`Writer` - модель записи пользователя__
  * _`key` - идентификатор пользователя_
  * _`step` - статус пользователя в диалоге_
  * _`cats` - количество съеденых котов_
  * _`breads` - количество съеденого хлеба_
* __`Message` - модель сообщения пользователя__
  * _`text` - текст сообщения_
  * _`answer` - текст ответа бота_
  * _`previous_id` - ссылка на прошлое сообщение_
  * _`write_id` - ссылка на запись пользователя_
  
В Swagger можно посмотреть документацию по API: `127.0.0.1:8000/api/docs/`  
В админ-панели также можно посмотреть на записи: `127.0.0.1:8000/api/docs/`  
В ![backend/apps/util/cat.py](https://github.com/aftern0on/django-bot-testing/blob/main/backend/apps/util/cat.py) можно посмотреть алгоритм диалога и распознование ошибок  
В ![backend/apps/bot/models.py](https://github.com/aftern0on/django-bot-testing/blob/main/backend/apps/bot/models.py) можно посмотреть описание моделей
