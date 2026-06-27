from django.db import models

from apps.app_users.models import CustomUser
from apps.app_currencies.models import Currency



class Account(models.Model):
    ACCOUNT_TYPES = (
    ('cash', 'Naqd'),
    ('card', 'Karta'),
    ('bank', 'Bank'),
)
    
    user = models.ForeignKey(to=CustomUser, verbose_name="Foydalanuvchi", related_name="accounts", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Hisob nomi", max_length=244)
    account_type = models.CharField(verbose_name="To'lov turi", max_length=4, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(verbose_name="Balans", default=0, max_digits=15, decimal_places=2)
    currency = models.ForeignKey(to=Currency, on_delete=models.PROTECT,related_name="currency_accounts", verbose_name="Valyuta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")


    def __str__(self):
        return f"{self.name} ({self.user})"


    class Meta:
        verbose_name = "Hisob"
        verbose_name_plural = "Hisoblar"