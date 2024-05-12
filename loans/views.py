from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Loans
from .form import LoansForm


@login_required
def loans(request):
    loans = Loans.objects.filter(user_id=request.user)
    return render(request, "loans.html", {
        'loans': loans
    })


def loan_create(request):
    if request.method == 'GET':
        form = LoansForm()
        return render(request, "loan_create.html", {
            "form": form,
        })
    else:
        try:
            form = LoansForm(request.POST)
            newLoan = form.save(commit=False)
            newLoan.user_id = request.user
            newLoan.save()
            return redirect("/loans")
        except ValueError:
            return render(request, "loan_create.html", {
                "form": form,
                "error": "Verifique los datos ingresados"
            })


@login_required
def loan_pay(request, loan_id):
    try:
        if request.method == 'GET':
            loan = get_object_or_404(Loans, pk=loan_id)
            form = LoansForm(instance=loan)
            return render(request, "loan_pay.html", {
                "loan": loan,
                "form": form,
            })
        else:
            loan = get_object_or_404(Loans, pk=loan_id)
            form = LoansForm(instance=loan)
            newValues = form.save(commit=False)
            # Se extrae el valor del post que mandamos desde el template
            amount_pay = Decimal(request.POST["amount_pay"])
            newValues.amount -= amount_pay
            # Si al restar el abono se liquida o queda negativo, entonces se elimina el deudor
            if newValues.amount == 0 or newValues.amount < 0:
                loan.delete()
                return redirect("/loans/")
            else:
                newValues.save()
                return render(request, "loan_pay.html", {
                    "loan": loan,
                    "form": form,
                    "success": f"Se ha abonado con exito la cantidad de {amount_pay}"
                })
    except ValueError:
        return render(request, "debt_pay.html", {
            "loan": loan,
            "form": form,
            "error": "Verifique los datos ingresados"
        })
