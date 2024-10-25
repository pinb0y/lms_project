from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payments-add'),
]
