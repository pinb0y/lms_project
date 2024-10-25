from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer