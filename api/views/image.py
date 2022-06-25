from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.models import UploadImage
from api.serializers import ImageSerializer


class ImageViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer
