from django.forms import ModelForm
from .models import Category

# Aqui se define la clase (plantilla) para el formulario de la aplicacion
class CategoryForm(ModelForm):
    # La clase Meta en un formulario se utiliza para proporcionar metadatos y configuración adicional
    class Meta:
        model = Category
        fields = ['name', 'description']
