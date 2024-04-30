from django.contrib import admin
from django.urls import path
from expense import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('expense/', views.expense, name='expense'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin')
]
