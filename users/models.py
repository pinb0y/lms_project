from django.contrib.auth.models import AbstractUser
from django.db import models

from studies.models import Course, Lesson


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
