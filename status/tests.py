from django.contrib.auth.models import User
from django.test import TestCase

from .models import Status


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='testuser@gmail.com')
        user.set_password('testing')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='testuser')
        obj = Status.objects.create(user=user, content='Test Content')
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)
