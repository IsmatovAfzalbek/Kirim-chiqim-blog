from django.db import models

from apps.app_users.models import CustomUser


class Category(models.Model):
    CATEGORY_TYPE = (
        ("income", "Daromad"),
        ("expense", "Xarajat")
    )
    
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="categories", verbose_name="Foydalanuvchi")
    name = models.CharField(max_length=100, verbose_name="Nomi")
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE, verbose_name="Kategoriya turi")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaratilgan vaqti")
    
    
    def __str__(self):
        return f"{self.name} ({self.category_type})"


    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
    
    
    
    
    
    
    
    
    
    
    