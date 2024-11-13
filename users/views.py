from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_sessions


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
