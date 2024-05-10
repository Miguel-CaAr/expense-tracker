from django.db import models
from django.contrib.auth.models import User


class Debts(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuario", on_delete=models.CASCADE)
    debtor_name = models.CharField(
        verbose_name="Nombre del deudor", max_length=100)
    description = models.TextField(
        verbose_name="Descripcion adicional", max_length=500)
    amount = models.DecimalField(
        verbose_name="Monto de la deuda", blank=False, null=False, max_digits=10, decimal_places=2)
    date_of_creation = models.DateTimeField(
        verbose_name="Fecha de creaicon", auto_now_add=True)

    class Meta:
        db_table = "Deudores"
        verbose_name = "Deudor"
        verbose_name_plural = "Deudores"

    def __str__(self) -> str:
        return f"{self.amount} - by {self.debtor_name} - to {self.user_id.username}"
