from django.contrib import admin
from .models import Expense

# ? Aqui utilice un decorador para registrar el modelo en el Admin de Django
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    # ? Aqui utilice un decorador para registrar el modelo en el Admin de Django
    fields = ['user_id', 'title', 'amount', 'description',
              'category_id', 'date_of_registration']
    # List Display es para definir que se mostrara en el listado del admin
    list_display = ['user_id', 'title', 'amount', 'description',
                    'category_id', 'date_of_registration']
    # Read Only Fields especifica los campos que seran solamente de lectura y no edicion
    readonly_fields = ("date_of_registration",)
