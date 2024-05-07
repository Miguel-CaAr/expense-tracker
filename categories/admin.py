from django.contrib import admin
from .models import Category

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['user_id', 'name', 'description', 'date_of_creation']
    list_display = ['user_id', 'name', 'description', 'date_of_creation']
    readonly_fields = ("date_of_creation",)
