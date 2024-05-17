from django.contrib import admin
from .models import Category

# Register your models here.

#? Aqui utilice un decorador para registrar el modelo en el Admin de Django
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #? Fields son los campos del modelo que deben mostrarse al editar
    fields = ['user_id', 'name', 'description', 'date_of_creation']
    #? List Display es para definir que se mostrara en el listado del admin
    list_display = ['user_id', 'name', 'description', 'date_of_creation']
    #? Read Only Fields especifica los campos que seran solamente de lectura y no edicion
    readonly_fields = ("date_of_creation",)
