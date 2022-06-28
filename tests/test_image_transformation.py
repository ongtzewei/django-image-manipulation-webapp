import json
from io import BytesIO
from django.conf import settings
from django.test import Client
from PIL import Image, ImageChops
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api.views.upload import UploadViewSet


class TestImageTransformation(APITestCase):

    original_image_path = settings.BASE_DIR / 'tests/resources/gears.png'
    jpeg_image_path = settings.BASE_DIR / 'tests/resources/gears.jpeg'
    rotated_image_path = settings.BASE_DIR / 'tests/resources/gears_r90.png'
    cropped_image_path = settings.BASE_DIR / 'tests/resources/gears_c350.png'
    resized_image_path = settings.BASE_DIR / 'tests/resources/gears_r350.png'
    masked_image_path = settings.BASE_DIR / 'tests/resources/gears_mblur.png'
    multiops_image_path = settings.BASE_DIR / 'tests/resources/gears_r500_c350_r180_mcontour.png'

    def setUp(self):
        self.original_image = Image.open(self.original_image_path)
        self.jpeg_image = Image.open(self.jpeg_image_path)
        self.rotated_image = Image.open(self.rotated_image_path)
        self.cropped_image = Image.open(self.cropped_image_path)
        self.resized_image = Image.open(self.resized_image_path)
        self.masked_image = Image.open(self.masked_image_path)
        self.multiops_image = Image.open(self.multiops_image_path)

        self.client = Client()
        self.factory = APIRequestFactory()
        with open(self.original_image_path, 'rb') as fp:
            request = self.factory.post('/api/images/', {'images[]': fp})
            view = UploadViewSet.as_view({'post': 'create'})
            response = view(request)
            self.image_id = response.data.get('images')[0].get('id')
        return super().setUp()

    def tearDown(self) -> None:
        self.original_image.close()
        self.jpeg_image.close()
        self.rotated_image.close()
        self.cropped_image.close()
        self.resized_image.close()
        self.masked_image.close()
        self.multiops_image.close()
        return super().tearDown()

    def test_no_op(self):
        request_url = '/api/images/{id}'.format(id=self.image_id)
        response = self.client.get(request_url)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNumQueries(1)
        self.assertEqual(json_response.get('id', None), self.image_id)

    def test_image_format(self):
        request_url = '/api/images/{id}.{fmt}'.format(id=self.image_id, fmt='jpg')
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.jpeg_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None

    def test_rotate_image(self):
        request_url = '/api/images/{id}.{fmt}?rotate={angle}'.format(id=self.image_id, fmt='png', angle=90)
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.rotated_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None

    def test_crop_image(self):
        request_url = '/api/images/{id}.{fmt}?crop={cropbox}'.format(id=self.image_id, fmt='png', cropbox='0,0,350,350')
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.cropped_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None

    def test_resize_image(self):
        request_url = '/api/images/{id}.{fmt}?resize={resize}'.format(id=self.image_id, fmt='png', resize='350x350')
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.resized_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None

    def test_mask_image(self):
        request_url = '/api/images/{id}.{fmt}?mask={mask}'.format(id=self.image_id, fmt='png', mask='blur')
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.masked_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None

    def test_multiple_ops(self):
        request_url = '/api/images/{id}.{fmt}?resize={resize}&crop={cropbox}&rotate={angle}&mask={mask}'\
            .format(id=self.image_id, fmt='png', resize='500x500', cropbox='0,0,250,350', angle=180, mask='contour')
        response = self.client.get(request_url)
        response_image = Image.open(BytesIO(response.content))
        diff = ImageChops.difference(self.multiops_image, response_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert diff.getbbox() is None
