from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Loans(models.Model):
    user_id = models.ForeignKey(
        User, verbose_name="ID del usuairo", on_delete=models.CASCADE)
    lender = models.CharField(
        verbose_name="Prestamista", blank=False, null=False, max_length=50)
    amount = models.DecimalField(
        verbose_name="Monto del prestamo", blank=False, null=False, max_digits=10, decimal_places=2)
    description = models.TextField(
        verbose_name="Descripcion del prestamo", blank=True, max_length=500)
    date_of_registration = models.DateTimeField(
        verbose_name="Fecha del registro", auto_now_add=True)

    class Meta:
        db_table = "Prestamos"
        verbose_name = "Prestamo"
        verbose_name_plural = "Prestamos"

    def __str__(self) -> str:
        return f"You owne ${self.amount} to {self.lender}"
