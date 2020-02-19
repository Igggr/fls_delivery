from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import FoodCategory, User
from app.forms import AuthForm,RegistrationForm


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
@login_required
def account():
    return render_template("account.html")


@app.route("/auth/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = AuthForm()
    if form.validate_on_submit():
        print("all ok")
        user = User.query.filter_by(mail=form.mail.data).first()
        if user and user.check_hash(form.password.data):
            login_user(user)
            return redirect(url_for("account"))
    return render_template('auth.html', form=form)


@app.route("/registration/", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            form.email.errors.append("Пользователь с таким ящиком уже существует.")
            render_template('auth.html', form=form,  registration_page=True)
        user = User()
        form.populate_obj(user)
        user.save()
        flash("Аккаунт успешно создан", "success")
        return redirect(url_for("account"))
    return render_template('auth.html', form=form,  registration_page=True)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

