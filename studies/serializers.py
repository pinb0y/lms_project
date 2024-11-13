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
    subscription = serializers.SerializerMethodField(read_only=True)


    def get_len_lessons(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        if obj.subscription_set.exists() and obj.owner == obj.subscription_set.first().user:
            return 'подписка оформлена'
        return 'нет подписки'

    class Meta:
        model = Course
        fields = ('id', 'title', 'owner', 'preview', 'description', 'len_lessons', 'lessons', 'subscription', 'price')


