from django.db import models
# Importacion del modelo `User` del módulo `models` en el paquete `auth` de Django. 
# Proporciona funcionalidades relacionadas con la autenticación y autorización de usuarios. 
# Contiene campos como nombre de usuario, contraseña, correo electrónico, etc.
from django.contrib.auth.models import User

# Modelo de datos, hereda de la clase las funcionalidades que permite interactuar con la BD
class Category(models.Model):
    # Campo de llave foranea "user_id" nombre del campo, y el resto es una expresion para los atributos
    user_id = models.ForeignKey(
    # 'User' es la relacion, 'verbose_name' para el admin, 'CASCADE' especifica la eliminacion en cascada
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    # Campo de tipo texto/cadena, con longitud maxima de 100 caracteres. 
    name = models.CharField(
        verbose_name="Nombre de la categoria", max_length=100)
    # Campo de tipo texto/cadena pero para textos mas largos, puede ser ilimitada.
    description = models.TextField(
        verbose_name="Descripcion de la categoria", max_length=500)
    # Campo de tipo fecha y hora, con argumento para establecer fecha y hora actual a la creacion
    date_of_creation = models.DateTimeField(
        verbose_name="Fecha de creaicon", auto_now_add=True)

    # Metadatos adicionales
    class Meta:
        db_table = "Categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    # Método de representacion de cadena que devuelve el nombre del objeto
    def __str__(self) -> str:
        return f"{self.name}"
