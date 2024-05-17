from django.forms import ModelForm
from .models import Expense

# Aqui se define la clase (plantilla) para el formulario de la aplicacion
class ExpenseForm(ModelForm):
    # La clase Meta en un formulario se utiliza para proporcionar metadatos y configuración adicional
    class Meta:
        model = Expense
        fields = ['amount', 'title', 'description', 'category_id',]
