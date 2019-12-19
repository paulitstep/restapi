import os
import shutil
import tempfile
from PIL import Image

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from status.models import Status


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class StatusAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='testuser@gmail.com')
        user.set_password('testing')
        user.save()

        status = Status.objects.create(user=user, content='Hello world!')

    def test_status(self):
        self.assertEqual(Status.objects.count(), 1)

    def status_user_token(self):
        auth_url = reverse('api-auth:login')
        auth_data = {
            'username': 'testuser',
            'password': 'testing'
        }
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data.get('token', 0)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_item(self):
        self.status_user_token()
        url = reverse('api-status:list')
        data = {
            'content': 'Hello world, part II'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    def test_empty_create_item(self):
        self.status_user_token()
        url = reverse('api-status:list')
        data = {
            'content': None,
            'image': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response.data

    def test_status_create_with_image(self):
        self.status_user_token()
        url = reverse('api-status:list')
        image = Image.new('RGB', (800, 1280), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as img:
            data = {
                'content': 'Hello world, part II',
                'image': img
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    def test_status_create_with_image_and_no_content(self):
        self.status_user_token()
        url = reverse('api-status:list')
        image = Image.new('RGB', (800, 1280), (0, 124, 174))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(tmp_file, format='JPEG')
        with open(tmp_file.name, 'rb') as img:
            data = {
                'content': '',
                'image': img
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Status.objects.count(), 2)
        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'testuser')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)

    def test_status_create(self):
        data = self.create_item()
        data_id = data.get('id')
        put_url = reverse('api-status:detail', kwargs={'pk': data_id})
        put_data = {
            'content': 'Hello world, part III'
        }

        get_response = self.client.get(put_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_status_update(self):
        data = self.create_item()
        data_id = data.get('id')
        put_url = reverse('api-status:detail', kwargs={'pk': data_id})
        put_data = {
            'content': 'Hello world, part III'
        }
        put_response = self.client.put(put_url, put_data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        put_response_data = put_response.data
        self.assertEqual(put_response_data['content'], put_data['content'])

    def test_status_delete(self):
        data = self.create_item()
        data_id = data.get('id')
        put_url = reverse('api-status:detail', kwargs={'pk': data_id})
        put_data = {
            'content': 'Hello world, part III'
        }
        delete_response = self.client.delete(put_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(put_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_no_token_create(self):
        url = reverse('api-status:list')
        data = {
            'content': 'Hello world, part II'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_permissions_api(self):
        data = self.create_item()
        data_id = data.get('id')
        user = User.objects.create(username='testuser1')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        put_url = reverse('api-status:detail', kwargs={'pk': data_id})
        put_data = {
            'content': 'REST API'
        }
        get_response = self.client.get(put_url, format='json')
        put_response = self.client.put(put_url, put_data, format='json')
        delete_response = self.client.delete(put_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
