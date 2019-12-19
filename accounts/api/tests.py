from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='testuser@gmail.com')
        user.set_password('testing')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='testuser')
        self.assertEqual(qs.count(), 1)

    def test_register_user_api_fail(self):
        url = reverse('api-auth:register')
        data = {
            'username': 'testuser_1',
            'email': 'testuser1@gmail.com',
            'password': 'testing1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password2'][0], 'This field is required.')

    def test_register_user_api(self):
        url = reverse('api-auth:register')
        data = {
            'username': 'testuser_1',
            'email': 'testuser1@gmail.com',
            'password': 'testing1',
            'password2': 'testing1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_len = len(response.data.get('token', 0))
        self.assertGreater(token_len, 0)

    def test_login_user_api(self):
        url = reverse('api-auth:login')
        data = {
            'username': 'testuser',
            'password': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertGreater(token_len, 0)

    def test_login_user_api_fail(self):
        url = reverse('api-auth:login')
        data = {
            'username': 'testuser1',  # does not exist
            'password': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        token = response.data.get('token', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)
        self.assertEqual(token_len, 0)

    def test_token_login_api(self):
        url = reverse('api-auth:login')
        data = {
            'username': 'testuser',
            'password': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_register_api(self):
        url = reverse('api-auth:login')
        data = {
            'username': 'testuser',
            'password': 'testing'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url2 = reverse('api-auth:register')
        data2 = {
            'username': 'testuser_1',
            'email': 'testuser1@gmail.com',
            'password': 'testing1',
            'password2': 'testing1'
        }
        response = self.client.post(url2, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
