from django.forms import ModelForm
from .models import Incomes


class IncomesForm(ModelForm):
    class Meta:
        model = Incomes
        fields = ['source', 'amount', 'description']
