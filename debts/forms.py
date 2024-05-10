from django.forms import ModelForm
from .models import Debts


class DebtsForm(ModelForm):
    class Meta:
        model = Debts
        fields = ['debtor_name', 'description', 'amount']
