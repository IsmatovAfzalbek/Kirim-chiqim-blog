from django.db import models

from apps.app_users.models import CustomUser
from apps.app_accounts.models import Account
from apps.app_categories.models import Category
from apps.app_currencies.models import Currency




FREQUENCY_CHOICES = (
    ('daily', 'Kunlik'),
    ('weekly', 'Haftalik'),
    ('monthly', 'Oylik'),
    ('yearly', 'Yillik'),
)


TRANSACTION_TYPE = (
    ('income', 'Daromad'),
    ('expense', 'Xarajat'),
)


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_transactions", verbose_name="Foydalanuvchi")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_transactions", verbose_name="Hisob")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_transactions", verbose_name="Kategoriya")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, verbose_name="Tranzaksiya turi")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="currency_transactions", verbose_name="Valyuta")
    amount_uzs = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa (so'mda)")
    description = models.TextField(blank=True, verbose_name="Izoh")
    date = models.DateField(verbose_name="Sana")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")


    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.currency})"


    class Meta:
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"
        ordering = ['-date']
        
        
        
class RecurringTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_recurring_transactions", verbose_name="Foydalanuvchi")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_recurring_transactions", verbose_name="Hisob")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_recurring_transactions", verbose_name="Kategoriya")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, verbose_name="Tranzaksiya turi")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="currency_recurring_transactions", verbose_name="Valyuta")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name="Takrorlanish")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(null=True, blank=True, verbose_name="Tugash sanasi")
    next_run_date = models.DateField(verbose_name="Keyingi bajarilish sanasi")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")


    def __str__(self):
        return f"{self.title} - {self.frequency}"


    class Meta:
        verbose_name = "Takrorlanuvchi tranzaksiya"
        verbose_name_plural = "Takrorlanuvchi tranzaksiyalar"
        ordering = ['-created_at']