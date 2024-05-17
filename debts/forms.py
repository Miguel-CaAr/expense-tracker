from django.forms import ModelForm
from .models import Debts

#? Aqui se define la clase (plantilla) para el formulario de la aplicacion
class DebtsForm(ModelForm):
    #? La clase Meta en un formulario se utiliza para proporcionar metadatos y configuración adicional
    class Meta:
        model = Debts
        fields = ['debtor_name', 'description', 'amount']
