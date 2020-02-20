from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, LoginManager
import os
from app.models import db, User, Order, Meal, FoodCategory


app = Flask(__name__)

app.config.from_object("app.config.DebugConfig")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URI']

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.logout_view = 'logout'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


admin = Admin(app, db)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(FoodCategory, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))

migrate = Migrate(app, db)


@app.context_processor
def utility_processor():
    def meals_in_basket():
        return sum(v for v in session['cart'].values())

    def basket_price():
        meals_costs = (Meal.query.get(int(id)).price * ammount for id, ammount in session['cart'].items())
        return sum(meals_costs)

    return {'meals_in_basket': meals_in_basket,
            'basket_price': basket_price}


@app.shell_context_processor
def shell_context():
    return {"db": db, "User": User, "Order": Order, "Meal": Meal, "FoodCategory": FoodCategory}


from app.views import *

if __name__ == "__main__":
    app.run()
