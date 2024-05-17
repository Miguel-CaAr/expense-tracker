from django.shortcuts import render, redirect, get_object_or_404  # Funciones para renderizar plantillas, redireccionar y obtener objetos o devolver un 404
from django.contrib.auth.decorators import login_required  # Decorador para restringir el acceso a usuarios autenticados
from decimal import Decimal  # Para trabajar con numeros decimales
from .models import Loans  # Importacion del modelo de prestamos
from .form import LoansForm  # Importacion del formulario de prestamos


@login_required  # Acceso a la vista solo a usuarios autenticados
def loans(request):  # Funcion para mostrar los prestamos
    loans = Loans.objects.filter(user_id=request.user)  # Se obtienen los prestamos relacionados con el usuario autenticado
    return render(request, "loans.html", {  # Se renderiza el listado de prestamos
        'loans': loans  # Se envian los datos
    })


@login_required  # Acceso a la vista solo a usuarios autenticados
def loan_create(request):  # Funcion para crear prestamos
    if request.method == 'GET':  # Si el metodo es 'GET'
        form = LoansForm()  # Se instancia el formulario
        return render(request, "loan_create.html", {  # Se renderiza el formulario en el template
            "form": form,  # Se envian los datos
        })
    else:  # Sino es 'GET'
        try:  # Bloque manejador de excepciones
            form = LoansForm(request.POST)  # Instancia del formulario con los datos 'POST'
            newLoan = form.save(commit=False)  # Se guardan los datos antes de ser guardados
            newLoan.user_id = request.user  # Se asigna el id del usuario autenticado al fk 'user_id'
            newLoan.save()  # Se guarda el formulario
            return redirect("/loans")  # Se redirecciona al listado
        except ValueError:  # En caso de error
            return render(request, "loan_create.html", {  # Se retorna la renderización del template
                "form": form,  # Con el formulario
                "error": "Verifique los datos ingresados"  # Y el mensaje de error
            })


@login_required  # Acceso a la vista solo a usuarios autenticados
def loan_pay(request, loan_id):  # Funcion para realizar pagos de prestamos, recibe el id del prestamo a pagar
    try:  # Bloque manejador de excepciones
        if request.method == 'GET':  # Si el metodo de la solicitud es 'GET'
            loan = get_object_or_404(Loans, pk=loan_id)  # Se obtiene el prestamo con la primary key recibida
            form = LoansForm(instance=loan)  # Se instancia el formulario con la instancia del prestamo
            return render(request, "loan_pay.html", {  # Se renderiza la pagina de pago del prestamo
                "loan": loan,  # Se envia el prestamo
                "form": form,  # Y el formulario
            })
        else:  # Si no es 'GET'
            loan = get_object_or_404(Loans, pk=loan_id)  # Se obtiene el prestamo con la primary key recibida
            form = LoansForm(instance=loan)  # Se instancia el formulario con la instancia del prestamo
            newValues = form.save(commit=False)  # Se guardan los nuevos valores antes de guardarlos
            # Se extrae el valor del pago del prestamo desde el formulario
            amount_pay = Decimal(request.POST["amount_pay"])
            newValues.amount -= amount_pay  # Se resta el pago al total del prestamo
            # Si el prestamo se liquida o queda con saldo negativo, se elimina
            if newValues.amount == 0 or newValues.amount < 0:
                loan.delete()  # Se elimina el prestamo
                return redirect("/loans/")  # Se redirecciona al listado de prestamos
            else:  # Si no se liquida completamente
                newValues.save()  # Se guardan los nuevos valores
                return render(request, "loan_pay.html", {  # Se renderiza la pagina de pago del prestamo
                    "loan": loan,  # Se envia el prestamo
                    "form": form,  # El formulario
                    "success": f"Se ha abonado con éxito la cantidad de {amount_pay}"  # Y un mensaje de éxito
                })
    except ValueError:  # En caso de error
        return render(request, "loan_pay.html", {  # Se renderiza la pagina de pago del prestamo
            "loan": loan,  # Se envia el prestamo
            "form": form,  # El formulario
            "error": "Verifique los datos ingresados"  # Y un mensaje de error
        })
