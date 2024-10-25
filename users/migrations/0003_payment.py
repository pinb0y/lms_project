# Generated by Django 4.2 on 2024-10-23 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0003_alter_lesson_preview'),
        ('users', '0002_alter_user_options_remove_user_username_user_avatar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now=True, verbose_name='Дата платежа')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Сумма платежа')),
                ('payment_method', models.CharField(choices=[('TRANSFER', 'денежный перевод'), ('CASH', 'Наличные деньги')], max_length=10, verbose_name='Способ оплаты')),
                ('payed_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studies.course', verbose_name='оплаченный курс')),
                ('payed_lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studies.lesson', verbose_name='оплаченный урок')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]