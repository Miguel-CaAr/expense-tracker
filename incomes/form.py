from django.forms import ModelForm
from .models import Incomes

# Aqui se define la clase (plantilla) para el formulario de la aplicacion
class IncomesForm(ModelForm):
    # La clase Meta en un formulario se utiliza para proporcionar metadatos y configuración adicional
    class Meta:
        model = Incomes
        fields = ['source', 'amount', 'description']
