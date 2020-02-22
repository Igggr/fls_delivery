from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask import redirect, url_for, request
from flask_login import current_user
from app import app, db
from app.models import User, FoodCategory, Meal, Order
from flask_admin.contrib.sqla import ModelView


class AdminOnly:

    def is_accessible(self):
       return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
       # redirect to login page if user doesn't have access
       return redirect(url_for('login', next=request.url))


class ProtectedModelView(AdminOnly, ModelView):
    pass


class DashboardView(AdminIndexView, AdminOnly):

    @expose('/')
    def index(self):
        return self.render('admin/dashboard_index.html')


    def is_accessible(self):
       return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
       # redirect to login page if user doesn't have access
       return redirect(url_for('login', next=request.url))


class StatsView(AdminOnly, BaseView):
    @expose('/')
    def index(self):
        orders = Order.query.all()
        users = User.query.all()
        return self.render('admin/stats/index.html', orders=orders, users=users)


class CustomerView(AdminOnly, BaseView):
    @expose('/<int:uid>/')
    def index(self,  uid):
        user = User.query.get(uid)
        return self.render('admin/customers/index.html')


class UserView(ProtectedModelView):
    column_exclude_list = ['_password_hash']
    column_searchable_list = ['address']

    can_create = False
    can_edit = True
    can_delete = True

    page_size = 50


class MealView(ProtectedModelView):
    column_searchable_list = ['description', 'price', 'title']
    column_filters = ["price", 'category']

    can_create = False
    can_edit = True
    can_delete = True

    page_size = 50


admin = Admin(app, db, index_view=DashboardView())

admin.add_view(StatsView(name='Статистика', endpoint='stats'))
admin.add_view(UserView(User, db.session))
admin.add_view(ProtectedModelView(FoodCategory, db.session))
admin.add_view(MealView(Meal, db.session))
admin.add_view(ProtectedModelView(Order, db.session))
