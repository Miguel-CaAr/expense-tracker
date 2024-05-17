from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Incomes
from .form import IncomesForm
import json


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes(request):
    incomes = Incomes.objects.filter(user_id=request.user)
    return render(request, "incomes.html", {
        'incomes': incomes
    })


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes_create(request):
    if request.method == 'GET':
        form = IncomesForm()
        return render(request, "income_create.html", {
            "form": form,
        })
    else:
        try:
            form = IncomesForm(request.POST)
            newIncome = form.save(commit=False)
            newIncome.user_id = request.user
            newIncome.save()
            return redirect("/incomes/")
        except ValueError:
            return render(request, "income_create.html", {
                "form": form,
                "error": "Verifique los datos ingresados"
            })


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes_by_source_chart(request):
    incomes = Incomes.objects.filter(user_id=request.user)
    income_sum_by_source = {}  # Diccionario para almacenar la suma de ingresos por fuente
    # Calcular la suma de ingresos por fuente
    for income in incomes:
        if income.source in income_sum_by_source:
            income_sum_by_source[income.source] += income.amount
        else:
            income_sum_by_source[income.source] = income.amount
    # Preparar los datos en el formato necesario para el gráfico
    data = [{"source": source, "amount": float(amount)}
            for source, amount in income_sum_by_source.items()]
    print(data)
    return render(request, "incomes_by_source_chart.html", {
        "data": json.dumps(data)  # Se manda como un JSON
    })


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def income_delete(request, income_id):
    income = get_object_or_404(Incomes, pk=income_id, user_id=request.user)
    if request.method == "POST":
        income.delete()
        return redirect("/incomes/") 
