from flask import render_template, redirect, url_for, flash, session, request
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user, login_required
from  sqlalchemy.sql.expression import func
from app import app
from app.models import FoodCategory, User, Meal, Order, OrderMealAssociation
from app.forms import AuthForm, RegistrationForm, CSRForm


@app.before_request
def set_session():
    if 'cart' not in session:
        session['cart'] = dict()


@app.route("/")
def index():
    categories = {}
    for category in FoodCategory.query:
        meals3 = Meal.query.filter(Meal.category == category).order_by(func.random()).limit(3)
        categories[category.title] = meals3
    return render_template('main.html', categories=categories)


@app.route("/stash_meal/<meal_id>/", methods=['POST'])
def add_to_cart(meal_id):
    """I think, that user should be able to add as many meals to basket as he want
    So this route just add meal  to basket and redirect back to where he came"""
    print(f'ref: {request.referrer}')
    meal = Meal.query.get(int(meal_id))
    flash(f'Блюдо {meal.title} добавлено в корзину', 'success')
    session['cart'].setdefault(meal_id, 0)
    session['cart'][meal_id] += 1  # if they want 3 portion of fried potatoes - let them
    return redirect(request.referrer)


@app.route('/remove_meal/<meal_id>/', methods=['POST'])
def remove_from_cart(meal_id):
    """user will only see this link if he has that meal in basket
    so - why check that he actually has?"""
    if session['cart'][meal_id] == 1:
        session['cart'].pop(meal_id)
    else:
        session['cart'][meal_id] -= 1
    session.modified = True
    flash(f"Блюдо {Meal.query.get(int(meal_id)).title} удалено из корзины", 'warning')
    return redirect(url_for('cart'))


class CartView(MethodView):
    methods = ['POST', 'GET']

    @staticmethod
    def get():
        form = CSRForm()
        return render_template('cart.html', Meal=Meal, form=form)

    @staticmethod
    def post():
        form = CSRForm()
        if form.validate_on_submit():
            order = Order(user_id=current_user.id)
            for meal_id, amount in session['cart'].items():
                association = OrderMealAssociation(orders=order, meals_id=int(meal_id), amount=amount)
            order.save()
            session['cart'].clear()
            flash('Заказ отправлен', 'success')
            return redirect(url_for('order_done'))
        else:
            return render_template('cart.html', Meal=Meal, form=form)


app.add_url_rule('/cart/', view_func=CartView.as_view("cart"))


@app.route('/order_done/')
def order_done():
    return render_template('ordered.html')


@app.route("/account/")
@login_required
def account():
    return render_template("account.html", orders=current_user.orders)


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
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('account')
            return redirect(next_page)
    return render_template('auth.html', form=form)


@app.route("/registration/", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:                     # TODO this mail check doesn't work. Fix it
            form.mail.errors.append("Пользователь с таким ящиком уже существует.")
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
    flash("Вы вышли", "primary")
    return redirect(url_for('login'))
