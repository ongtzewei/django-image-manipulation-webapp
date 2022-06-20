import base64
import urllib3
from io import BytesIO
from PIL import Image as PILImage
from rest_framework import status, viewsets
from rest_framework.response import Response
from api.models import TransformedImage
from api.serializers import TransformedImageSerializer

http = urllib3.PoolManager()

class TransformedImageViewSet(viewsets.ModelViewSet):
    queryset = TransformedImage.objects.all()
    serializer_class = TransformedImageSerializer

    def create(self, request, *args, **kwargs):
        to_process = request.data
        image_to_process = 'image' in kwargs and kwargs['image'] or request.data.get('image', None)
        to_process['source'] = isinstance(image_to_process, str) and \
          TransformedImage.ImageSource.Remote or TransformedImage.ImageSource.Upload
        
        to_process['source_path'] = ''
        if (to_process['source'] == TransformedImage.ImageSource.Remote):
          to_process['source_path'] = image_to_process
        
        to_process['original_file'] = image_to_process
        to_process['transformed_file'] = TransformedImageViewSet.apply_transformations(image_to_process)

        print(to_process)
        serializer = self.get_serializer(data=to_process)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @classmethod
    def apply_transformations(self, image_to_process):
        return image_to_process
