from rest_framework import viewsets, generics
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from studies.models import Course, Lesson
from studies.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)