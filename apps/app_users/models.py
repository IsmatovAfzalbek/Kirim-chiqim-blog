from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email majburiy!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    objects = CustomUserManager() 
    email = models.EmailField(verbose_name="Email", unique=True, max_length=49)
    created_at = models.DateTimeField(verbose_name="Yaratilgan vaqt", auto_now_add = True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    
    class Meta:
        verbose_name = "Shaxs"
        verbose_name_plural = "Shaxslar"
        
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"