from django.contrib import admin
from django.urls import path
from expense import views
from categories import views as views_categories
from debts import views as views_debts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    #----------LOGIN AND REGISTER----------#
    path('signup/', views.signup, name="signup"),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    #----------EXPENSES----------#
    path('expense/', views.expense, name='expense'),
    path('expense/create/', views.expense_create, name='expense_create'),
    path('expense/update/<int:expense_id>', views.expense_update, name='expense_update'),
    path('expense/update/delete/<int:expense_id>', views.expense_delete, name='expense_delete'),
    #----------CATEGORIES----------#
    path('categories/create/', views_categories.category_create, name='category_create'),
    path('chart/expenses-by-category/',views_categories.expenses_by_category_chart, name="expenses_by_category_chart"),
    #----------DEBTS----------#
    path('debts/', views_debts.debts, name="debts"),
    path('debts/create/', views_debts.debts_create, name="debts_create"),
    path('debt/pay/<int:debt_id>', views_debts.debt_pay, name="debt_pay"),
]
