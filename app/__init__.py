from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from app.models import db, User, Order, Meal, FoodCategory


app = Flask(__name__)

app.config.from_object("app.config.DebugConfig")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URI']

db.init_app(app)
admin = Admin(app, db)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(FoodCategory, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))

migrate = Migrate(app, db)

@app.shell_context_processor
def shell_context():
    return {"db": db, "User": User, "Order": Order, "Meal": Meal, "FoodCategory": FoodCategory}


from app.views import *

if __name__ == "__main__":
    app.run()
