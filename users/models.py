from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(
        max_length=30, verbose_name="Телефон", blank=True, null=True
    )
    city = models.CharField(
        max_length=100, verbose_name="Город", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="users/avatar", verbose_name="Аватарка", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)
