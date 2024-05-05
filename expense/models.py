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
        return f"{self.name} - by {self.user_id.username}"


class Expense(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name="Monto del gasto", max_digits=10, decimal_places=2)
    description = models.TextField(
        verbose_name="Descripcion del monto", blank=True, max_length=500)
    category_id = models.ForeignKey(
        Category, verbose_name="Categoria del gasto", on_delete=models.SET_NULL, null=True)
    date_of_registration = models.DateTimeField(
        verbose_name="Fecha del registro", auto_now_add=True)

    class Meta:
        db_table = "Gastos"
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self) -> str:
        return f"{self.description} - by {self.user_id.username}"
