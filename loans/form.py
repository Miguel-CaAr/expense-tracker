from django.forms import ModelForm
from .models import Loans

# Aqui se define la clase (plantilla) para el formulario de la aplicacion
class LoansForm(ModelForm):
    # La clase Meta en un formulario se utiliza para proporcionar metadatos y configuración adicional
    class Meta:
        model = Loans
        fields = ['lender', 'amount', 'description']
