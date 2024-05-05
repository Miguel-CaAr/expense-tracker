from django.contrib import admin
from django.urls import path
from expense import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('expense/', views.expense, name='expense'),
    path('expense/create/', views.expense_create, name='expense_create'),
    path('expense/update/<int:expense_id>', views.expense_update, name='expense_update'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
