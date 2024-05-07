from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import ExpenseForm
from .models import Expense
from categories.models import Category


def home(request):
    return render(request, "home.html")

# ----------LOGIN AND REGISTER----------#


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

# ----------EXPENSES----------#


@login_required
def expense(request):
    expenses = Expense.objects.filter(user_id=request.user)
    return render(request, 'expense.html', {
        "expenses": expenses,
    })


@login_required
def expense_create(request):
    if request.method == 'GET':
        form = ExpenseForm()
        form.fields["category_id"].queryset = Category.objects.filter(
            user_id=request.user)
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


@login_required
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


@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, user_id=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("/expense/")
