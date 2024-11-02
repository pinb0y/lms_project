from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, views, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from studies.models import Course, Lesson, Subscription
from studies.paginators import LessonPaginator
from studies.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.models import User
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonPaginator

    def perform_create(self, serializer):
        if isinstance(self.request.user, User):
            serializer.save(owner=self.request.user)
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsModerator | IsOwner,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)

    def perform_create(self, serializer):
        if isinstance(self.request.user, User):
            serializer.save(owner=self.request.user)
        serializer.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = (IsAuthenticated,)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)


class SubscriptionAPIView(views.APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_item = get_object_or_404(Course, pk=kwargs['pk'])

        subs, _ = Subscription.objects.get_or_create(user=user, course=course_item)

        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course_item.title} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course_item = get_object_or_404(Course, pk=kwargs['pk'])
        Subscription.objects.filter(user=self.request.user, course=course_item).delete()
        response = {
            'detail': f'Курс {course_item.title} удален из подписок',
        }
        return Response(response, status.HTTP_204_NO_CONTENT)
