from django.forms import ModelForm
from .models import Expense

class ExpenseForm(ModelForm):
  class Meta:
    model = Expense
    fields = ['amount', 'description', 'category_id',]
    # list_display = ['user_id', 'amount', 'description', 'category_id', 'date_of_registration']
    # readonly_fields = ("date_of_registration",)