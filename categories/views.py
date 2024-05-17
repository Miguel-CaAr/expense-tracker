from django.shortcuts import render, redirect #? Funciones para renderizar y redirigir respectivamente
from django.contrib.auth.decorators import login_required #? Decorador proteger rutas
from .forms import CategoryForm #? Formulario de 'Categorias'
from categories.models import Category #? Modelo de 'Categorias'
from expense.models import Expense #? Modelo de 'Gastos'
import json #? es un módulo para codificar y decodificar datos en formato JSON.

# ----------CATEGORIES----------#
@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
#? Funcion que toma una solicitud de Django como param
def category_create(request):
    #? Estructura condicional que verifica si el metodo de la solicitud es 'GET'
    if (request.method == "GET"):
        #? Instancia del formulario de 'Categoria'
        form = CategoryForm()
        #? Retorna la renderizacion de la plantilla y se pasa el formulario como contexto
        return render(request, "category_create.html", {
            "form": form,
        })
    #? Sino se cumple el if
    else:
        #? Estructura para manejar excepciones
        try:
            #? Instancia del formulario con los datos 'POST'
            form = CategoryForm(request.POST)
            #? Se utiliza .save para obtener los datos del formulario y crear una instancia del modelo Category sin guardarla en la base de datos todavía
            newCategory = form.save(commit=False)
            #? Asigna el usuario actual al campo 'user_id' de la nueva categoría
            newCategory.user_id = request.user
            #? Guarda la nueva categoría en la base de datos
            newCategory.save()
            #? Retorna la redirreccion al formulario de creacion de gasto
            return redirect("/expense/create")
        #? Excepcion en caso de que el error sea de tipo ValueError
        except ValueError:
            #? Si hay un error se renderiza el formulario de creaicon de categoria con un mensaje
            return render(request, "category_create.html", {
                "form": form,
                "error": "Verifique los datos ingresados"
            })
            
@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
#? Funcion que toma la solicitud de como param
def expenses_by_category_chart(request):
    #? Instancia de los datos de 'Categorias', filtro para traer datos donde el id sea el del usuario logeado
    categories = Category.objects.filter(user_id = request.user)
    #? Instancia de los datos de 'Gastos', filtro para traer datos donde el id sea el del usuario logeado
    expenses = Expense.objects.filter(user_id = request.user)
    #? Se declara una lista para almacenar las categorias con los totales de los gastos relacionados 
    data = []
    #? Itera en cada categoria de la instancia a 'Categorias'
    for category in categories:
        #? Variable para almacenar los totales de gastos segun categoria
        totalExpenses = 0
        #? Iterador para gasto en la instancia de 'Gastos'
        for expense in expenses:
            #? Condicional, si el gasto se relaciona con la categoria
            if expense.category_id == category:
                #? Asgnacion adicion del monto del gasto convertido a float
                totalExpenses += float(expense.amount)
        #? '.append' metodo para agregar al final de la lista la categoria una vez terminado el ciclo
        #? con el total de gastos que tienen la relacion con la categoria
        data.append({"id": category.id, "name": category.name, "total": totalExpenses})
    #? Se retorna la renderizacion de la grafica con los datos convertidos en JSON para ser
    #? facilmente manipulables por JavaScript
    return render(request, "expenses_by_category_chart.html", {
        "data": json.dumps(data) #Se manda como un JSON
        })