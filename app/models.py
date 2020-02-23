from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum
from datetime import datetime


db = SQLAlchemy()


class SaveMixin:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()


class OrderStatus(Enum):
    AWAITING_PAYMENT = 0
    PREPARING = 10
    IN_DELIVERY = 20
    DELIVERED = 30


class UserRole(Enum):
    USER = 1
    ADMIN = 100


class User(db.Model, UserMixin, SaveMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    orders = db.relationship("Order", back_populates="user")
    _role = db.Column(db.Integer, nullable=False, default=UserRole.USER.value)

    UserRole = UserRole

    @property
    def password(self):
        raise AttributeError("Мы заботимся о сохранности паролей)))")

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def check_hash(self, plaintext):
        return check_password_hash(self._password_hash, plaintext)

    @property
    def role(self):
        return UserRole(self._role)

    @role.setter
    def role(self, role_enum):
        self.role = role_enum.value


class OrderMealAssociation(db.Model):
    __tablename__ = 'order_meal_associations'
    meals_id = db.Column(db.Integer, db.ForeignKey("meals.id"), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)

    orders = db.relationship('Order', back_populates='meals')
    meals = db.relationship('Meal', back_populates="orders")


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
    orders = db.relationship(OrderMealAssociation, back_populates="meals")


class Order(db.Model, SaveMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    meals = db.relationship(OrderMealAssociation, back_populates="orders")
    user = db.relationship(User, back_populates="orders")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    _status = db.Column(db.Integer, default=OrderStatus.AWAITING_PAYMENT.value, nullable=False)

    OrderStatus = OrderStatus

    @property
    def total_price(self):
        return sum([m.meals.price * m.amount for m in self.meals])

    @total_price.setter
    def total_price(self, price):
        raise ValueError("don't cheat on us")

    @property
    def status(self):
        return OrderStatus(self._status)

    @status.setter
    def status(self, enum_status):
        self._status = enum_status.value
