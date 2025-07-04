import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session

dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    ROOT_DB_USER = os.getenv("DB_USER", "postgres")
    ROOT_DB_PASSWORD = os.getenv("DB_PASSWORD")

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    MAX_CONTENT_LENGTH = 10*1024*1024
    MAX_FORM_MEMORY_SIZE = 1024 * 1024  # 1MB
    MAX_FORM_PARTS = 500    
    
    NAME_RESTAURNAT = "Kazoku Sushi 寿司"

    def uri_postgres(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DATABASE_NAME}"

    def uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"


config = DatabaseConfig()


# Налаштування бази даних Postgres
engine = create_engine(config.uri_postgres(), echo=True)
Session_db = scoped_session(sessionmaker(bind=engine))

# Декларація базового класу для моделей, Необхідно для реалізації відношень у ORM
class Base(DeclarativeBase):
    def create_db(self):
        """
        Ініціалізація метаданих,
        створює базу даних, якщо відсутня,
        створює таблиці на основі моделей(що спадкуються від Base),
        якщо жодної немає
        """
        self.metadata.create_all(engine)

    def drop_db(self):
        """
        Деструкція метаданих,
        видаляє базу даних, якщо така наявна,
        видаляє усі таблиці
        """
        self.metadata.drop_all(engine)