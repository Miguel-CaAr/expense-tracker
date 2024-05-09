from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class Expense(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name="Monto del gasto", blank=False, null=False,max_digits=10, decimal_places=2)
    title = models.CharField(
        verbose_name="Titulo del gasto", blank=False, null=False, max_length=50)
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
        return f"{self.title} - by {self.user_id.username}"
