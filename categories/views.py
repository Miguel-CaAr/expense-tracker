from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm
from expense.models import Expense
from categories.models import Category
import json

# ----------CATEGORIES----------#


@login_required
def category_create(request):
    if (request.method == "GET"):
        form = CategoryForm()
        return render(request, "category_create.html", {
            "form": form,
        })
    else:
        try:
            form = CategoryForm(request.POST)
            newCategory = form.save(commit=False)
            newCategory.user_id = request.user
            newCategory.save()
            return redirect("/expense/create")
        except ValueError:
            return render(request, "category_create.html", {
                "form": form,
                "error": "Verifique los datos ingresados"
            })
            
@login_required
def expenses_by_category_chart(request):
    categories = Category.objects.filter(user_id = request.user)
    expenses = Expense.objects.filter(user_id = request.user)
    data = []
    for category in categories:
        totalExpenses = 0
        for expense in expenses:
            if expense.category_id == category:
                totalExpenses += float(expense.amount)
        data.append({"id": category.id, "name": category.name, "total": totalExpenses})
    return render(request, "expenses_by_category_chart.html", {
        "data": json.dumps(data) #Se manda como un JSON
        })