from django.contrib import admin
from .models import Expense, Category
# Register your models here.

@admin.register(Category)
class ExpenseAdmin(admin.ModelAdmin):
  fields = ['user_id', 'name', 'description', 'date_of_creation']
  list_display = ['user_id', 'name', 'description', 'date_of_creation']
  readonly_fields = ("date_of_creation",)
  
@admin.register(Expense)
class CategoryAdmin(admin.ModelAdmin):
  fields = ['user_id', 'amount', 'description', 'category_id', 'date_of_registration']
  list_display = ['user_id', 'amount', 'description', 'category_id', 'date_of_registration']
  readonly_fields = ("date_of_registration",)