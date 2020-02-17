from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from datetime import datetime

db = SQLAlchemy()


class _OrderStatus(Enum):
    awaiting_payment = 0
    preparing = 1
    in_delivery = 2
    delivered = 3
    canceled = 4
    in_dispute = 5


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    orders = db.relationship("Order", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Мы заботимся о сохранности паролей)))")

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def check_hash(self, plaintext):
        return check_password_hash(self._password_hash, plaintext)


order_meals_association = db.Table("order_meals",
                                   db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
                                   db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),)


class FoodCategory(db.Model):
    __tablename__ = "food_categories"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)

    meals = db.relationship("Meal", back_populates="category")


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String)
    picture = db.Column(db.String)

    category_id = db.Column(db.String, db.ForeignKey("food_categories.id"))

    category = db.relationship("FoodCategory", back_populates="meals")
    orders = db.relationship("Order", back_populates="meals", secondary=order_meals_association)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    meals = db.relationship(Meal, back_populates="orders", secondary=order_meals_association)
    user = db.relationship(User, back_populates="orders")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    status = _OrderStatus

    @property
    def total_price(self):
        return sum([m.price for m in self.meals])

    @total_price.setter
    def total_price(self, price):
        raise ValueError("don't cheat on us")

