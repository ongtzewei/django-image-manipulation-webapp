from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.views.image import ImageViewSet


class TestLocalUpload(TestCase):
    def test_local_upload(self):
        factory = APIRequestFactory()
        request = factory.post('/api/transform-image/', {'image': ['/tmp/yoda.png']})
        response = ImageViewSet.as_view({'post':'create'})(request._request)
        print(response.status_code)

