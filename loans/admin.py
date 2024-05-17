from django.contrib import admin
from .models import Loans

# Register your models here.

#? Aqui utilice un decorador para registrar el modelo en el Admin de Django
@admin.register(Loans)
class LoansAdmin(admin.ModelAdmin):
    #? Fields son los campos del modelo que deben mostrarse al editar
    fields = ['user_id', 'lender', 'amount', 'description', 'date_of_registration']
    #? List Display es para definir que se mostrara en el listado del admin
    list_display = ['user_id', 'lender', 'amount', 'description', 'date_of_registration']
    #? Read Only Fields especifica los campos que seran solamente de lectura y no edicion
    readonly_fields = ("date_of_registration",)
