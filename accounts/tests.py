from django.contrib.auth.models import User
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='testuser@gmail.com')
        user.set_password('testing')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='testuser')
        self.assertEqual(qs.count(), 1)
