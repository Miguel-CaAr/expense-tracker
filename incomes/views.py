from django.shortcuts import render, redirect, get_object_or_404 # Funciones para renderizar plantillas, redireccionar y obtener objetos o devolver un 404
from django.contrib.auth.decorators import login_required # Decorador para restringir el acceso a usuarios autenticados
from .models import Incomes # Modelo de los ingresos
from .form import IncomesForm # Formulario de los ingresos
import json # Metodo para convertir en JSON


@login_required # Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes(request): # Funcion para mostrar los ingresos
    incomes = Incomes.objects.filter(user_id=request.user) # Se obtienen los datos que tengan relacion con el usuario autenticado
    return render(request, "incomes.html", { # Se renderiza el listado de ingresos
        'incomes': incomes # Se mandan los datos
    })


@login_required # Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes_create(request): # Funcion para crear ingresos
    if request.method == 'GET': # Si el metodo es 'GET'
        form = IncomesForm() # Se instancia el formulario
        return render(request, "income_create.html", { # Se renderiza el formulario en el template
            "form": form, # Datos
        })
    else: # Sino es 'GET'
        try: # Bloque manejador de excepciones
            form = IncomesForm(request.POST) # Instancia del formulario con los datos 'POST'
            newIncome = form.save(commit=False) # Se guardan los datos antes de ser guardados
            newIncome.user_id = request.user # Se asigna el id del usuario auth al fk 'user_id'
            newIncome.save() # Se guarda el formulario
            return redirect("/incomes/") # Se redirecciona al listado
        except ValueError: # En caso de error
            return render(request, "income_create.html", { # Se retorna la renderizacion del template
                "form": form, # Con el formulario
                "error": "Verifique los datos ingresados" # Y el msj de error
            })


@login_required # Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def incomes_by_source_chart(request): # Funcion para la grafica de ingresos
    incomes = Incomes.objects.filter(user_id=request.user) # Ingresos que sean del usuario autenticado
    income_sum_by_source = {}  # Diccionario para almacenar la suma de ingresos por fuente
    # Calcular la suma de ingresos por fuente
    for income in incomes:  # Itera por cada ingreso en la lista incomes
        if income.source in income_sum_by_source:  # Si la fuente del ingreso está en el diccionario income_sum_by_source
            # Asigna-adiciona el monto del ingreso al valor existente en income_sum_by_source para la fuente correspondiente
            income_sum_by_source[income.source] += income.amount
        else:
            # Si la fuente del ingreso no se encuentra en el diccionario, agrega una nueva entrada con el monto del ingreso actual
            income_sum_by_source[income.source] = income.amount
            
    # Preparar los datos en el formato necesario para el gráfico
    # Cada elemento del diccionario se convierte en un diccionario en la lista 'data', donde:
    # - La clave 'source' corresponde a la fuente del ingreso.
    # - La clave 'amount' corresponde a la cantidad de ingresos, convertida a tipo flotante.
    data = [{"source": source, "amount": float(amount)} 
    # Se itera sobre los elementos del diccionario 'income_sum_by_source' para formatear los datos.
            for source, amount in income_sum_by_source.items()]
    print(data) #? Aqui imprimí para visualizar los datos y corroborar que estuvieran bien
    return render(request, "incomes_by_source_chart.html", { # Se renderiza la grafica
        "data": json.dumps(data)  # Se mandan los datos como un JSON
    })


@login_required # Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def income_delete(request, income_id): # Funcion para eliminar el ingreso, recibe el id del ingreso a eliminar
    # Se obtiene el ingreso donde la primary key es el id recibido y el foreign key es el id del usuario auth
    income = get_object_or_404(Incomes, pk=income_id, user_id=request.user)
    if request.method == "POST": # Si el metodo de la solicitud es 'POST'
        income.delete() # Se elimina el ingreso
        return redirect("/incomes/") # Se redirecciona al listado
