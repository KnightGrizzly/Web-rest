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
    
    reservations = relationship("Reservation", 
                                foreign_keys="Reservation.user_id", 
                                back_populates="user",
                                cascade="all, delete-orphan")
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

class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    time_start: Mapped[datetime] = mapped_column(DateTime)
    type_table: Mapped[str] = mapped_column(String(20))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship("User", foreign_keys="Reservation.user_id", back_populates="reservations")


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_list: Mapped[dict] = mapped_column(JSONB)
    order_time: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

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
        name = "Burger",
        weight = "300",
        ingredients = "булка, котлета теляча, сир, помідор, соус, лук, зелнь",
        description = "Соковитий бургер",
        price = 250, 
        file_name = "burger.jpg",
    )
    
    m2 = Menu(
        name = "Салат з лососем",
        weight = "150",
        ingredients = "Лосось, мікс салатів, кунжут, соус",
        description = "Салат дууууже смачний!!!",
        price = 145, 
        file_name = "salad.jpg",
    )
    

    with Session_db() as conn:
        conn.add_all([user_admin, m1, m2])
        conn.commit()


if __name__ == "__main__":
    init_db()