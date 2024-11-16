from rest_framework import serializers

from studies.models import Course, Lesson, Subscription
from studies.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='video_url'),
            serializers.UniqueTogetherValidator(fields=['title'], queryset=Lesson.objects.all())
        ]

class SubscriptionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = Subscription
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    len_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    sign_up = serializers.SerializerMethodField(source='subscription_course', read_only=True)


    def get_len_lessons(self, obj):
        return obj.lessons.count()

    def get_sign_up(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user).filter(course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'


