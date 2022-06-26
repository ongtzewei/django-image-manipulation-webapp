from django.conf import settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import UploadImage, UploadRequest
from api.utils import retrieve_remote_image
from rest_framework.test import APIRequestFactory
from api.views.upload import UploadViewSet
from api.views import transform_image

class TestImageTransformation(APITestCase):

    original_image = settings.BASE_DIR / 'tests/resources/bay.jpg'
    rotated_image = settings.BASE_DIR / 'tests/resources/bay.jpg'
    
    def setUp(self):
        self.factory = factory = APIRequestFactory()
        with open(self.original_image, 'rb') as fp:
            request = self.factory.post('/api/images/', {'images[]': fp})
            view = UploadViewSet.as_view({'post': 'create'})
            response = view(request)
            self.image_id = response.data.get('images')[0].get('id')
            print(self.image_id)
        return super().setUp()
    
    def test_rotate_image(self):
        request = self.factory.get('/api/images/{id}.{format}'.format(id=self.image_id, format='jpg'), {'rotate': '90'})
        print(request)
        view = transform_image(request, pk=self.image_id, format='jpeg')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNumQueries(1)
        self.assertEqual(response, self.rotated_image)
        
        
