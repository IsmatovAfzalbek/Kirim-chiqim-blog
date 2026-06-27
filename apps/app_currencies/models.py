from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Valyuta kodi")
    name = models.CharField(max_length=100, verbose_name="Valyuta nomi")
    symbol = models.CharField(max_length=10, verbose_name="Belgi")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Valyuta"
        verbose_name_plural = "Valyutalar"



class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Valyuta")
    rate_uzs = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Kurs (so'mda)")
    date = models.DateField(verbose_name="Sana")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")


    class Meta:
        verbose_name = "Valyuta kursi"
        verbose_name_plural = "Valyuta kurslari"
        unique_together = ['currency', 'date']
        
        
    def __str__(self):
        return f"{self.currency.code} - {self.rate_uzs} so'm ({self.date})"

