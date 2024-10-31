from rest_framework import serializers

from studies.models import Course, Lesson
from studies.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='video_url'),
            serializers.UniqueTogetherValidator(fields=['title'], queryset=Lesson.objects.all())
        ]


class CourseSerializer(serializers.ModelSerializer):
    len_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_len_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'len_lessons', 'lessons', 'owner')
