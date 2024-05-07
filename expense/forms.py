from django.forms import ModelForm
from .models import Expense


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category_id',]
