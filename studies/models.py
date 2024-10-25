from django.db import models


class Course(models.Model):
    title = models.CharField('Название', max_length=500, help_text='Название курса')
    preview = models.ImageField('Картинка', upload_to='course/preview', help_text='Картинка курса',
                                blank=True, null=True)
    description = models.TextField('Описание', null=True, blank=True, help_text='Описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title}'

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название', max_length=500, help_text='Название урока', default='урок')
    preview = models.ImageField('Картинка', upload_to='lesson/preview', help_text='Картинка урока',
                                blank=True, null=True)
    description = models.TextField('Описание', null=True, blank=True, help_text='Описание урока')
    video_url = models.URLField('Ссылка на видео', null=True, blank=True, help_text='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title}'