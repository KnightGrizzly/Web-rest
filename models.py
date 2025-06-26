from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import String, select, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash
from sqlalchemy.dialects.postgresql import JSONB
from settings import Base, Session_db


class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    orders = relationship("Orders", 
                            foreign_keys="Orders.user_id",
                            back_populates='user', 
                            cascade="all, delete-orphan")

    def __str__(self):
        return f"User: {self.username}"

    @staticmethod
    def get(user_id: int):
        with Session_db() as conn:
            stmt = select(User).where(User.id == user_id)
            user = conn.scalar(stmt)
            if user:
                return user

    @staticmethod
    def get_by_username(username):

        with Session_db() as conn:
            # stmt = select(User).where(User.username == username)
            stmt = select(User).filter_by(username = username)
            user = conn.scalar(stmt)
            return user if user else None

class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    weight: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    
    file_name: Mapped[str] = mapped_column(String)


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_list: Mapped[dict] = mapped_column(JSONB)
    order_time: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    status: Mapped[str] = mapped_column(default = "active")     # "disable", "compile"

    user = relationship("User", foreign_keys="Orders.user_id", back_populates="orders")


# Ініціалізація бази даних і додавання товарів
def init_db():
    base = Base()
    base.drop_db()
    base.create_db()  # Створюємо таблиці

    user_admin = User(
        username="admin", 
        email="ax@gmail.com", 
        password=generate_password_hash("admin"),
        is_admin=True
    )
    
    m1 = Menu(
        name = "Каліфорнія з крабом",
        weight = "220",
        ingredients = "Крабовий мікс, огірок, авокадо, ікра масаго",
        description = "Соковита каліфорнія",
        price = 165, 
        # file_name = 
    )
    m2 = Menu(
        name = "Філадульфія з лососем",
        weight = "210",
        ingredients = "Лосось, вершковий сир, огірок",
        description = "Соковита філадельфія",
        price = 185, 
        # file_name = 
     )
    m3 = Menu(
        name = "Спайсі тунець",
        weight = "200",
        ingredients = "Тунець, спайсі соус, авокадо",
        description = "Соковитий тунець",
        price = 175, 
        # file_name = 
    )    
    m4 = Menu(
        name = "Огірковий рол",
        weight = "180",
        ingredients = "Огірок, кунжут, водорості норі",
        description = "Соковита рол",
        price = 110, 
        # file_name = 
    )


    m5 = Menu(
        name = "Каліфорнія з крабом",
        weight = "220",
        ingredients = "Крабовий мікс, огірок, авокадо, ікра масаго",
        description = "Соковита каліфорнія",
        price = 165, 
        # file_name = 
    )
    m6 = Menu(
        name = "Каліфорнія з крабом",
        weight = "220",
        ingredients = "Крабовий мікс, огірок, авокадо, ікра масаго",
        description = "Соковита каліфорнія",
        price = 165, 
        # file_name = 
    )
    m7 = Menu(
        name = "Каліфорнія з крабом",
        weight = "220",
        ingredients = "Крабовий мікс, огірок, авокадо, ікра масаго",
        description = "Соковита каліфорнія",
        price = 165, 
        # file_name = 
    )


    m8 = Menu(
        name = "Чука салат",
        weight = "120",
        ingredients = "Морські водорості, горіховий соус",
        description = "Смачний салат",
        price = 95, 
        # file_name = 
    )
    m9 = Menu(
        name = "Салат з лососем",
        weight = "150",
        ingredients = "Лосось, мікс салатів, кунжут, соус",
        description = "Смачний салат",
        price = 145, 
        # file_name = 
    )


    m10 = Menu(
        name = "Місо суп",
        weight = "300",
        ingredients = "Тофу, вакасаме, зелена цибуля",
        description = "Смачний суп",
        price = 75, 
        # file_name = 
    )
    m11 = Menu(
        name = "Суп з лососем",
        weight = "350",
        ingredients = "Лосось, овочі, соєвий бульйон",
        description = "Смачний суп",
        price = 110, 
        # file_name = 
    )


    m12 = Menu(
        name = "Зелений чай",
        weight = "300",
        description = "Гарячий/холодний чай",
        price = 45, 
        # file_name = 
    )
    m13 = Menu(
        name = "Газована вода",
        weight = "500",
        description = "Холодна вода",
        price = 40, 
        # file_name = 
    )
    m14 = Menu(
        name = "Морс журавлинний",
        weight = "300",
        description = "Смачний напій",
        price = 50, 
        # file_name = 
    )


    with Session_db() as conn:
        conn.add_all([user_admin, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14])
        conn.commit()


if __name__ == "__main__":
    init_db()