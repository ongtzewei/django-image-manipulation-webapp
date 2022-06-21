from enum import Enum
from PIL import Image, ImageFilter
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from api.models import UploadImage
from api.serializers import ImageSerializer


class MaskFilter(Enum):
    BLUR = ImageFilter.BLUR
    CONTOUR = ImageFilter.CONTOUR
    DETAIL = ImageFilter.DETAIL
    EDGE_ENHANCE = ImageFilter.EDGE_ENHANCE
    EDGE_ENHANCE_MORE = ImageFilter.EDGE_ENHANCE_MORE
    EMBOSS = ImageFilter.EMBOSS
    FIND_EDGES = ImageFilter.FIND_EDGES
    SMOOTH = ImageFilter.SMOOTH
    SMOOTH_MORE = ImageFilter.SMOOTH_MORE
    SHARPEN = ImageFilter.SHARPEN


class ImageViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = ImageSerializer

    @action(detail=True, methods=['get'])
    def transform(self, request, pk=None):
        instance = self.get_object()
        image = Image.open(instance.original_file)
        
        resize = request.query_params.get('resize', None)
        if resize:
          resize_to = map(int, resize.split('x'))
          image = image.resize(resize_to, resample=Image.Resampling.NEAREST)

        crop = request.query_params.get('crop', None) 
        if crop:
          crop_to = list(map(int, crop.split(',')))
          image = image.crop(crop_to)
        
        mask = request.query_params.get('mask', None)
        if mask:
          mask_to_apply = MaskFilter[mask.upper()].value
          image = image.filter(mask_to_apply)
        
        serializer = self.get_serializer(instance, data={
          'transformed_file': image
        }, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


