from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from api.models import UploadImage, UploadRequest
from api.utils.helpers import retrieve_remote_image


# test cases to include
# upload local image
# upload local images
# upload remote image
# upload remote images
# rotate image 
# resize image 
# crop image 
# apply filter image




class TestLocalUpload(APITestCase):

    jpeg_image = settings.BASE_DIR / 'tests/resources/stock.jpeg'
    png_image = settings.BASE_DIR / 'tests/resources/gears.png'

    def setUp(self):
      self.client = APIClient()
      self.image = Image.open(self.png_image)
      return super().setUp()


    def test_upload_local_image(self):
      with open(self.png_image, 'rb') as fp:
        response = self.client.post('/api/images/', {'images[]': fp})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNumQueries(1)
        self.assertEqual(UploadImage.objects.count(), 1)
        self.assertEqual(UploadRequest.objects.count(), 1)

    def test_upload_multiple_local_images(self):
      fps = []
      for file in [ self.jpeg_image, self.png_image ]:
        fp = open(file, 'rb')
        fps.append(fp)
      response = self.client.post('/api/images/', {'images[]': fps})
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertNumQueries(1)
      self.assertEqual(UploadImage.objects.count(), 2)
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
