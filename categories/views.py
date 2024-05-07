from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm

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
            return redirect("/expense/")
        except ValueError:
            return render(request, "category_create.html", {
                "form": form,
                "error": "Verifique los datos ingresados"
            })
