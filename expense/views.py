from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ExpenseForm
from .models import Expense, Category

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


def expense_create(request):
    if request.method == 'GET':
        form = ExpenseForm()
        form.fields["category_id"].queryset = Category.objects.filter(user_id=request.user)
        return render(request, "expense_create.html", {
            'form': form
        })
    else:
        try:
            form = ExpenseForm(request.POST)
            new_expense = form.save(commit=False)
            new_expense.user_id = request.user
            new_expense.save()
            return redirect("/expense/")
        except ValueError:
            return render(request, "expense_create.html", {
                'form': ExpenseForm,
                'error': "Verifique los datos ingresados"
            })


def expense_update(request, expense_id):
    if request.method == 'GET':
        expense = get_object_or_404(Expense, pk=expense_id)
        form = ExpenseForm(instance=expense)
        return render(request, "expense_update.html", {
            "expense": expense,
            "form": form
        })
    else:
        expense = get_object_or_404(Expense, pk=expense_id)
        form = ExpenseForm(request.POST, instance=expense)
        form.save()
        return redirect("expense")        


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
