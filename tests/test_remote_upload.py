from unittest import mock
from django.conf import settings
from PIL import Image
from more_itertools import side_effect
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from api.models import UploadImage, UploadRequest
from api.utils import retrieve_remote_image
from rest_framework.test import APIRequestFactory
from api.views.upload import UploadViewSet


remote1_image = settings.BASE_DIR / 'tests/resources/remote_1.jpg'
remote2_image = settings.BASE_DIR / 'tests/resources/remote_2.bmp'
remote3_image = settings.BASE_DIR / 'tests/resources/remote_3.png'

def mocked_remote_image_response(url):
    return Image.open(remote1_image)
    

def mocked_remote_images_response(url):
    return [
        Image.open(remote1_image),
        Image.open(remote2_image),
        Image.open(remote3_image)
    ]


class TestRemoteUpload(APITestCase):
    jpg_image = 'https://static.euronews.com/articles/stories/05/11/96/34/1000x563_cmsv2_f011c436-f441-5294-98c9-dc907789220a-5119634.jpg'
    bmp_image = 'https://govinsider.asia/wp-content/uploads/2018/01/VirtualSingapore8.bmp'
    png_image = 'https://www.nicepng.com/png/full/419-4194049_singapore-skyline-png-singapore-colored-vector.png'

    def setUp(self):
        self.factory = factory = APIRequestFactory()
        self.image = self.jpg_image
        self.images = [
            self.bmp_image,
            self.png_image,
            self.jpg_image,
        ]
        return super().setUp()

    @mock.patch('urllib3.PoolManager.request', side_effect=mocked_remote_image_response)
    def test_upload_remote_image(self):
        request = self.factory.post('/api/images/', {'images': self.image})
        view = UploadViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNumQueries(1)
        self.assertEqual(UploadImage.objects.count(), 1)
        self.assertEqual(UploadRequest.objects.count(), 1)
    
    @mock.patch('urllib3.PoolManager.request', side_effect=mocked_remote_images_response)
    def test_upload_multiple_remote_images(self):
        request = self.factory.post('/api/images/', {'images': self.images})
        view = UploadViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNumQueries(1)
        self.assertEqual(UploadImage.objects.count(), 3)
        self.assertEqual(UploadRequest.objects.count(), 1)

    '''
    def test_upload_remote_image(self):
      fps = []
      client = APIClient()
      response = client.post('/api/images/', {'images': [
        "https://resources.matcha-jp.com/resize/720x2000/2020/11/13-109314.jpeg",
      ]})
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertNumQueries(1)
      self.assertEqual(UploadImage.objects.count(), 1)
      self.assertEqual(UploadRequest.objects.count(), 1)
    '''

    def test_transform_image(self):
      print(self.image)
