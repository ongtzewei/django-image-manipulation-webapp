from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from api.models import UploadImage, UploadRequest
from api.serializers import UploadSerializer
from api.serializers.image_serializer import ImageSerializer


class UploadViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = UploadRequest.objects.all()
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        serializer_data = {}
        processed_images = []

        request_data = request.data
        images_to_process = 'images[]' in request_data and \
          request.FILES.getlist('images[]') or request_data.get('images',[])
        for image_to_process in images_to_process:
          transformed_image = UploadViewSet.process_image(image_to_process)
          processed_images.append(transformed_image['id'])

        serializer_data['images_id'] = bool(processed_images) and processed_images or None
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @classmethod
    def process_image(cls, image):
        serializer_data = {}
        image_to_process = image
        serializer_data['source'] = isinstance(image_to_process, str) and \
          UploadImage.ImageSource.Remote or UploadImage.ImageSource.Upload

        serializer_data['source_path'] = ''
        if serializer_data['source'] == UploadImage.ImageSource.Remote:
          serializer_data['source_path'] = image_to_process

        serializer_data['original_file'] = image_to_process
        serializer_data['transformed_file'] = None
        image_serializer = ImageSerializer(data=serializer_data)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()
        return image_serializer.data
