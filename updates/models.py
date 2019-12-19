import json

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import models


def upload_update_image(instance, filename):
    return f'updates/{instance.user}/{filename}'


class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     return serialize('json', qs, fields=('user', 'content', 'image'))

    def serialize(self):
        list_values = list(self.values('id', 'user', 'content', 'image'))
        return json.dumps(list_values)


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, self._db)


class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UpdateManager()

    def __str__(self):
        return self.content or ''

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ''
        data = {
            'id': self.id,
            'user': self.user.id,
            'content': self.content,
            'image': image
        }
        data = json.dumps(data)
        return data
