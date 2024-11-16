from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone

from config import settings

from studies.models import Subscription, Course
from users.models import User


@shared_task
def update_notification(course_pk):
    """Отправка сообщения об обновлении курса по подписке"""

    course = Course.objects.filter(pk=course_pk).first()

    users = User.objects.all()
    for user in users:
        subscription = Subscription.objects.filter(course=course_pk, user=user.pk).first()

        if subscription:
            send_mail(
                subject=f'Обновление курса "{course}"',
                message=f'Курс "{course}", на который вы подписаны, обновлен.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    """Проверка последнего входа пользователей и отключение неактивных пользователей"""

    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')
