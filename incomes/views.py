from django.shortcuts import render


def incomes(request):
    return render(request, "incomes.html")
