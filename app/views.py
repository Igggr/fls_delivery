from flask import render_template
from app import app
from app.models import Meal, FoodCategory

@app.route("/")
def index():
    categories = {}
    for category in FoodCategory.query:
        categories[category.title] = category.meals[:3]
    return render_template('main.html', categories=categories)


@app.route("/cart/")
def cart():
    return "card"


@app.route("/account/")
def account():
    return "account"


@app.route("/login/")
def login():
    return "login"


@app.route('/logout/')
def logout():
    return "logout"

