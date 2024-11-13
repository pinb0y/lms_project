from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from studies.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


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

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('TRANSFER', 'денежный перевод'),
        ('CASH', 'Наличные деньги'),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, blank=True, null=True)
    payment_date = models.DateField(verbose_name='Дата платежа', auto_now=True)
    payed_course = models.ForeignKey(Course, verbose_name='оплаченный курс', on_delete=models.SET_NULL, blank=True,
                                     null=True)
    payed_lesson = models.ForeignKey(Lesson, verbose_name='оплаченный урок', on_delete=models.SET_NULL, blank=True,
                                     null=True)
    amount = models.PositiveSmallIntegerField(verbose_name='Сумма платежа')
    payment_method = models.CharField(verbose_name='Способ оплаты', max_length=10, choices=PAYMENT_METHODS)
    session_id = models.CharField(max_length=255, verbose_name='id сессии', blank=True, null=True)
    link = models.URLField(max_length=400, verbose_name='ссылка для платежа', blank=True, null=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.amount
