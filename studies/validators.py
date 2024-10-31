import re

from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = 'youtube'
        tmp_val = dict(value).get(self.field)

        if tmp_val and url not in tmp_val:
            raise ValidationError('only youtube links available')
