from enum import Enum
from time import time
from urllib.parse import parse_qsl
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse
from api.models import UploadImage
from PIL import Image, ImageFilter
from api.serializers.image_serializer import ImageSerializer
from api.utils import generate_random_filename


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


def transform_image(request, pk, format):
    instance = UploadImage.objects.get(pk=pk)
    if not format or format not in settings.ALLOWED_IMAGE_FORMATS:
        return HttpResponseRedirect(reverse('uploadimage-detail', kwargs={'pk': pk}))
    
    image = Image.open(instance.original_file)
    transform_ops = parse_qsl(request.META.get('QUERY_STRING'))
    for op_key, op_value in transform_ops:
        match op_key:
            case 'resize':
                resize_to = map(int, op_value.split('x'))
                image = image.resize(resize_to, resample=Image.Resampling.NEAREST)
            case 'crop':
                crop_to = list(map(int, op_value.split(',')))
                image = image.crop(crop_to)
            case 'mask':
                mask_to_apply = MaskFilter[op_value.upper()].value
                image = image.filter(mask_to_apply)
            case 'rotate':
                image = image.rotate(int(op_value))

    # save image to volume
    path_to_transformed_image = '/tmp/{filename}.{fmt}'.format(fmt=format, filename=generate_random_filename())
    image.save(path_to_transformed_image, format=format)
    serializer = ImageSerializer(instance, data={
        'transformed_file': image
    }, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response = HttpResponse(content_type='image/{format}'.format(format=format))
    image.save(response, format)
    return response