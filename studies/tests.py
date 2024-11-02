from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from studies.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование КРУД урока"""
    def setUp(self) -> None:
        self.user = User.objects.create(email='pin@boy.er')
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title='test lesson', description='test desc', owner=self.user)

    def test_delete_lesson(self):
        """Тестирование удаление урока"""

        url = reverse('studies:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_create_lesson(self):
        """Тестирование создание урока"""

        data = {
            'title': 'тестовый урок',
            'description': 'тестовое описание',
        }

        url = reverse('studies:lesson-create')
        response = self.client.post(url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'тестовый урок', 'preview': None, 'description': 'тестовое описание', 'video_url': None,
             'course': None, 'owner': 1}
        )

        self.assertEqual(Lesson.objects.all().count(), 2)

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование вывода листа уроков"""
        url = reverse('studies:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{'id': 4, 'title': 'test lesson', 'preview': None, 'description': 'test desc', 'video_url': None,
              'course': None, 'owner': 3}]
        )

    def test_update_lesson(self):
        """Тестирование обновление урока"""

        update_data = {
            'title': 'test_update',
            'description': 'test_update',
        }
        url = reverse('studies:lesson-update', args=(self.lesson.pk,))
        response = self.client.patch(url, data=update_data)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('description'),
            'test_update'

        )

    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""
        url = reverse('studies:lesson-get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('title'),
            self.lesson.title
        )


class TestsSubscription(APITestCase):
    """Тестирование создания и удаления модели подписки"""
    def setUp(self):
        self.user = User.objects.create(email='pin@boy.er')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='test course', description='test desc')

    def test_subscribe_user_success(self):
        """Тестирование на успешное создание подписки"""
        self.client.force_login(self.user)
        url = reverse('studies:subscription-post', args=(self.course.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_user_success(self):
        """Тестирование на успешное удаление подписки"""
        self.client.force_login(self.user)
        url = reverse('studies:subscription-post', args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)