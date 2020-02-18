from flask import render_template, redirect, url_for
from app import app
from app.models import FoodCategory
from app.forms import AuthForm


@app.route("/")
def index():
    categories = {}
    for category in FoodCategory.query:
        categories[category.title] = category.meals[:3]
    return render_template('main.html', categories=categories)


@app.route("/cart/")
def cart():
    return render_template('cart.html')


@app.route("/account/")
def account():
    return render_template("account.html")


@app.route("/auth/", methods=["POST", "GET"])
def login():
    form = AuthForm()
    print(form.email.data)
    print(form.password.data)
    if form.validate_on_submit():
        print("all ok")
        return redirect(url_for("account"))
    return render_template('auth.html', form=form)


@app.route('/logout/')
def logout():
    return redirect(url_for('login'))

