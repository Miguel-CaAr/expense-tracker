from django.contrib import admin
from django.urls import path
from expense import views

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
    path('categories/create/', views.category_create, name='category_create'),
]
