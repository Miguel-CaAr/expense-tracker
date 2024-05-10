from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Debts
from .forms import DebtsForm


@login_required
def debts_create(request):
    if (request.method == "GET"):
        form = DebtsForm()
        return render(request, "debts_create.html", {
            "form": form,
        })
    else:
        try:
            form = DebtsForm(request.POST)
            newDebts = form.save(commit=False)
            newDebts.user_id = request.user
            newDebts.save()
            return redirect("/debts/")
        except ValueError:
            return render(request, "debts_create.html", {
                "form": form,
                "eror": "Verifique los datos ingresados"
            })


@login_required
def debts(request):
    debts = Debts.objects.filter(user_id=request.user)
    return render(request, 'debts.html', {
        "debts": debts,
    })

@login_required
def debt_pay(request, debt_id):
    try:
        if request.method == 'GET':
            debt = get_object_or_404(Debts, pk=debt_id)
            form = DebtsForm(instance=debt)
            return render(request, "debt_pay.html", {
                "debt": debt,
                "form": form,
            })
        else:
            debt = get_object_or_404(Debts, pk=debt_id)
            form = DebtsForm(instance=debt)
            newValues = form.save(commit=False)
            #Se extrae el valor del post que mandamos desde el template
            amount_pay = Decimal(request.POST["amount_pay"])
            newValues.amount -= amount_pay
            #Si al restar el abono se liquida o queda negativo, entonces se elimina el deudor
            if newValues.amount == 0 or newValues.amount < 0:
                debt.delete()
                return redirect("/debts/")
            else:
                newValues.save()
                return render(request, "debt_pay.html", {
                    "debt": debt,
                    "form": form,
                    "success": f"Se ha abonado con exito la cantidad de {amount_pay}"
                })
    except ValueError: 
        return render(request, "debt_pay.html", {
            "debt": debt,
            "form": form,
            "error": "Verifique los datos ingresados"
        })