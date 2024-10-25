from rest_framework import serializers

from studies.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    len_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_len_lessons(self, obj):
        return obj.lessons.count()


    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'len_lessons', 'lessons')
