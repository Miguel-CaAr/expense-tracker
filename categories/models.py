from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name="Nombre de la categoria", max_length=100)
    description = models.TextField(
        verbose_name="Descripcion de la categoria", max_length=500)
    date_of_creation = models.DateTimeField(
        verbose_name="Fecha de creaicon", auto_now_add=True)

    class Meta:
        db_table = "Categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self) -> str:
        return f"{self.name}"
