from django.db import models
#? Importacion del modelo `User` del módulo `models` en el paquete `auth` de Django. 
#? Proporciona funcionalidades relacionadas con la autenticación y autorización de usuarios. 
#? Contiene campos como nombre de usuario, contraseña, correo electrónico, etc.
from django.contrib.auth.models import User

#? Modelo de datos, hereda de la clase las funcionalidades que permite interactuar con la BD
class Debts(models.Model):
    #? Campo de llave foranea "user_id" nombre del campo, y el resto es una expresion para los atributos
    user_id = models.ForeignKey(
        #? 'User' es la relacion, 'verbose_name' para el admin, 'CASCADE' especifica la eliminacion en cascada
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    #? Campo de tipo texto/cadena, con longitud maxima de 100 caracteres. 
    debtor_name = models.CharField(
        verbose_name="Nombre del deudor", max_length=100)
    #? Campo de tipo texto/cadena pero para textos mas largos, puede ser ilimitada.
    description = models.TextField(
        verbose_name="Descripcion adicional", max_length=500)
    #? Campo de tipo decimal, no puede ser vacio, no nulo, max digitos y numero de digitos decimales respectivamente.
    amount = models.DecimalField(
        verbose_name="Monto de la deuda", blank=False, null=False, max_digits=10, decimal_places=2)
    #? Campo de tipo fecha y hora, con argumento para establecer fecha y hora actual a la creacion
    date_of_creation = models.DateTimeField(
        verbose_name="Fecha de creaicon", auto_now_add=True)
    
    #? Metadatos adicionales
    class Meta:
        db_table = "Deudores"
        verbose_name = "Deudor"
        verbose_name_plural = "Deudores"
    #? Método de representacion de cadena que devuelve el nombre del monto, deudor y n. usuario
    def __str__(self) -> str:
        return f"{self.amount} - by {self.debtor_name} - to {self.user_id.username}"
