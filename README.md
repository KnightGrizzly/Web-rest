# веб ресторан `kazoku sushi`🍣
Веб-додаток на Python для замовлення їжі.
## Опис📖

**Веб Ресторан** дозволяє:
- Переглядати меню.
- Додавати страви до кошика та оформляти замовлення.
- Керувати меню через адмін-панель (для адміністраторів).

### Технології📄
- Python 3.8+
- Flask
- PostgreSQL
- HTML, CSS, JavaScript



# бібліотеки📕
1. Flask
2. Flask-Login
3. psycopg2
4. python-dotenv
5. SQLAlchemy
6. Flask-wtf
## створення .env📁
```
    DB_USER = <postgres_user>
    DB_PASSWORD = <postgres_passw>
    DATABASE_NAME = "restaurant_db"

    ROOT_DB_USER = "your_postgres_user"
    ROOT_DB_PASSWORD = "your_pg_pass"

    SECRET_KEY = "pass"
```
## 3.створення бази даних🗂️

1) **Postgres**: 
```
py pg_create_database.py
```
## 4.інструкція по запуску📋
1. Скачати проект
2. Перейти у папку з проектом
3. створення .venv
4. Встановлення бібліотек за командою `pip install -r requirements.txt`
5. Додати файл `.env` з вашими даними
6. створення бази данних через файл `pg_create_database.py`
7. Запуск доданку