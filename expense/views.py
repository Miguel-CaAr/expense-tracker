from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ExpenseForm
from .models import Expense

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'GET':
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('expense')
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "El usuario ya existe"
                })
        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Las contraseñas no coinciden"
        })


def expense(request):
    expenses = Expense.objects.filter(user_id=request.user)
    return render(request, 'expense.html', {
        "expenses" : expenses,
    })


def create_expense(request):    
    if request.method == 'GET':
        return render(request, "create_expense.html", {
            'form': ExpenseForm
        })
    else:
        try:
            form = ExpenseForm(request.POST)
            form.user = request.user
            form.save()
            return redirect("/expense/")
        except ValueError:
            return render(request, "create_expense.html", {
                'form': ExpenseForm,
                'error': "Verifique los datos ingresados"
            })

def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == 'GET':
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "El usuario o la contraseña es incorrecta"
            })
        else:
            login(request, user)
            return redirect("/expense")
