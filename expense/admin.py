from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    fields = ['user_id', 'title', 'amount', 'description',
              'category_id', 'date_of_registration']
    list_display = ['user_id', 'title', 'amount', 'description',
                    'category_id', 'date_of_registration']
    readonly_fields = ("date_of_registration",)
