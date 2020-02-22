from flask_admin import Admin
from app import app, db
from app.models import User, FoodCategory, Meal, Order
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, db)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(FoodCategory, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))
