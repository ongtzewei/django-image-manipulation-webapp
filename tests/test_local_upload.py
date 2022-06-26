from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from api.models import UploadImage, UploadRequest
from api.utils import retrieve_remote_image
from rest_framework.test import APIRequestFactory
from api.views.upload import UploadViewSet

class TestLocalUpload(APITestCase):
    jpg_image = settings.BASE_DIR / 'tests/resources/bay.jpg'
    jpeg_image = settings.BASE_DIR / 'tests/resources/stock.jpeg'
    png_image = settings.BASE_DIR / 'tests/resources/gears.png'

    def setUp(self):
        self.factory = factory = APIRequestFactory()
        self.image = self.png_image
        self.images = [
            self.png_image,
            self.jpeg_image,
            self.jpg_image,
        ]
        return super().setUp()

    def test_upload_local_image(self):
        with open(self.image, 'rb') as fp:
            request = self.factory.post('/api/images/', {'images[]': fp})
            view = UploadViewSet.as_view({'post': 'create'})
            response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNumQueries(1)
        self.assertEqual(UploadImage.objects.count(), 1)
        self.assertEqual(UploadRequest.objects.count(), 1)
    
    def test_upload_multiple_local_images(self):
        fps = []
        for file in self.images:
            fp = open(file, 'rb')
            fps.append(fp)
        
        request = self.factory.post('/api/images/', {'images[]': fps})
        view = UploadViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNumQueries(1)
        self.assertEqual(UploadImage.objects.count(), 3)
        self.assertEqual(UploadRequest.objects.count(), 1)
