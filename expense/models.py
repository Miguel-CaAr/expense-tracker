from django.db import models
# Importacion del modelo `User` del módulo `models` en el paquete `auth` de Django. 
# Proporciona funcionalidades relacionadas con la autenticación y autorización de usuarios. 
# Contiene campos como nombre de usuario, contraseña, correo electrónico, etc.
from django.contrib.auth.models import User
from categories.models import Category

# Modelo de datos, hereda de la clase las funcionalidades que permite interactuar con la BD
class Expense(models.Model):
    # Campo de llave foranea "user_id" nombre del campo, y el resto es una expresion para los atributos
    user_id = models.ForeignKey(
        # 'User' es la relacion, 'verbose_name' para el admin, 'CASCADE' especifica la eliminacion en cascada
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    # Campo de tipo decimal, no puede ser vacio, no nulo, max digitos y numero de digitos decimales respectivamente.
    amount = models.DecimalField(
        verbose_name="Monto del gasto", blank=False, null=False,max_digits=10, decimal_places=2)
    # Campo de tipo texto/cadena, con longitud maxima de 100 caracteres. 
    title = models.CharField(
        verbose_name="Titulo del gasto", blank=False, null=False, max_length=50)
    # Campo de tipo texto/cadena pero para textos mas largos, puede ser ilimitada.
    description = models.TextField(
        verbose_name="Descripcion del monto", blank=True, max_length=500)
    # Campo de tipo llave foranea, al elimnarse la categoria el campo queda como nulo, nulo permitido, respectivamente.
    category_id = models.ForeignKey(
        Category, verbose_name="Categoria del gasto", on_delete=models.SET_NULL, null=True)
    # Campo de tipo fecha y hora, con argumento para establecer fecha y hora actual a la creacion
    date_of_registration = models.DateTimeField(
        verbose_name="Fecha del registro", auto_now_add=True)
    
    # Metadatos adicionales
    class Meta:
        db_table = "Gastos"
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
    # Método de representacion de cadena que devuelve el nombre del monto, deudor y n. usuario
    def __str__(self) -> str:
        return f"{self.title} - by {self.user_id.username}"
