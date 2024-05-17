from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Debts
from .forms import DebtsForm


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def debts_create(request): #? Funcion, de param recibe la solicitud
    if (request.method == "GET"): #? Condicional si el metodo de solicitud es 'GET'
        form = DebtsForm() #? Instancia del formulario
        return render(request, "debts_create.html", { #? Funcion para renderizar la plantilla HTML
            "form": form, #? Diccionario con los datos
        })
    else:
        try: #? Bloque para manejar excepcion
            form = DebtsForm(request.POST) #? Instancia del formulario con la solicitud 'POST'
            newDebts = form.save(commit=False) #? Instancia del form antres de guardarse
            newDebts.user_id = request.user #? Asignacion del usuario logeado como user_id
            newDebts.save() #? Guardadp del formulario
            return redirect("/debts/") #? Redireccion al listado de deudas
        except ValueError: #? Excepcion en caso de error
            return render(request, "debts_create.html", { #?Renderiza el formulario de crear deuda
                "form": form, #? Diccionario con datos
                "eror": "Verifique los datos ingresados" #? Dato de error
            })


@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def debts(request): #? Funcion con solicitud
    debts = Debts.objects.filter(user_id=request.user) #? Instancia de los datos que coincidan con el id del user logeado
    return render(request, 'debts.html', { #? Renderizacion del listado de deudas
        "debts": debts, #? Datos de deudas
    })

@login_required #? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
def debt_pay(request, debt_id): #? Funcion que recibe la solicitud y el id de deuda
    try: #? Bloque para manejar excepcion
        if request.method == 'GET': #? Condicion si la solicitud es 'GET'
            debt = get_object_or_404(Debts, pk=debt_id)#? Se obtiene la deuda que su primary key sea igual al id recibido como param
            #? De no ser asi se utiliza el methodo 'get_object_or_404' para mandar error 404 not found
            
            form = DebtsForm(instance=debt) #? Instancia del formulario con la instanacia de  datos de la deuda
            return render(request, "debt_pay.html", { #? Retorno de renderizacion del pago con diccionario
                "debt": debt, #? Dato de la deuda
                "form": form, #? Formulario
            })
        else: #? En caso de no ser 'GET' la solicitud
            debt = get_object_or_404(Debts, pk=debt_id) #? Se obtiene la deuda que su primary key sea igual al id recibido como param
            #? De no ser asi se utiliza el methodo 'get_object_or_404' para mandar error 404 not found
            
            form = DebtsForm(instance=debt) #? Instnaia del form con la instancia de datos de deuda
            newValues = form.save(commit=False)
            amount_pay = Decimal(request.POST["amount_pay"]) #? Se extrae el 'amount_pay' del 'POST' que mandamos desde el template
            newValues.amount -= amount_pay #? Asignacion decremento del 'amount_pay' a los nuevos valores
            if newValues.amount == 0 or newValues.amount < 0:#? Si al restar el abono se liquida o queda negativo, entonces se elimina el deudor
                debt.delete() #? Se elimina la deuda
                return redirect("/debts/") #? Se redirecciona al listao de deudas
            else: #? En caso de no superar o ser igual al valor de la deuda
                newValues.save() #? Se guarda la deuda con el 'newValues.amount' restado
                return render(request, "debt_pay.html", { #? Retorno de renderizacion de template
                    "debt": debt, #? Dato de pago
                    "form": form, #? Formulario
                    "success": f"Se ha abonado con exito la cantidad de {amount_pay}" #? Mensaje de hecho
                })
    except ValueError: #? En caso de excpcion tipo ValueError
        return render(request, "debt_pay.html", { #? Renderiza la misma pagina
            "debt": debt, #? Con dato de deuda
            "form": form, #? Formulario
            "error": "Verifique los datos ingresados" #? Pero se manda mensaje de error
        })