from django.db import models
from django.contrib.auth.models import User


class Incomes(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuairo", on_delete=models.CASCADE)
    amount = models.DecimalField(
        verbose_name="Monto del ingreso", blank=False, null=False, max_digits=10, decimal_places=2)
    source = models.CharField(
        verbose_name="Fuente de ingreso", blank=False, max_length=50)
    description = models.TextField(
        verbose_name="Descripcion del prestamo", blank=True, max_length=500)
    date_of_registration = models.DateTimeField(
        verbose_name="Fecha del registro", auto_now_add=True)

    class Meta:
        db_table = "Ingresos"
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self) -> str:
        return f"You earned ${self.amount} from {self.source}"