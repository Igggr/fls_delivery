from flask import Flask
from flask_migrate import Migrate
import os
from app.models import db, User, Order, Meal, FoodCategory


app = Flask(__name__)

app.config.from_object("app.config.DebugConfig")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URI']

db.init_app(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def shell_context():
    return {"db": db, "User": User, "Order": Order, "Meal": Meal, "FoodCategory": FoodCategory}


from app.views import *
