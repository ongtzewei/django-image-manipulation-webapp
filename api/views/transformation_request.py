from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from api.models import TransformationRequest, TransformedImage
from api.serializers import TransformationRequestSerializer
from api.serializers.transformed_image_serializer import TransformedImageSerializer


class TransformationRequestViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = TransformationRequest.objects.all()
    serializer_class = TransformationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer_data = {}
        processed_images = []

        transformation_request = request.data
        images_to_process = 'images[]' in transformation_request and \
          request.FILES.getlist('images[]') or transformation_request.get('images',[])
        for image_to_process in images_to_process:
          transformed_image = TransformationRequestViewSet.transform_image(image_to_process)
          processed_images.append(transformed_image['id'])

        serializer_data['images_id'] = bool(processed_images) and processed_images or None
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @classmethod
    def transform_image(cls, image):
        serializer_data = {}
        image_to_process = image
        serializer_data['source'] = isinstance(image_to_process, str) and \
          TransformedImage.ImageSource.Remote or TransformedImage.ImageSource.Upload

        serializer_data['source_path'] = ''
        if serializer_data['source'] == TransformedImage.ImageSource.Remote:
          serializer_data['source_path'] = image_to_process
        
        serializer_data['original_file'] = image_to_process
        serializer_data['transformed_file'] = image_to_process
        #serializer_data['transformed_file'] = TransformedImageViewSet.apply_transformations(image_to_process)
        image_serializer = TransformedImageSerializer(data=serializer_data)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()
        return image_serializer.data
